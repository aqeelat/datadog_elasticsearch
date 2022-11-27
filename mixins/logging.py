from django.utils import timezone


class Logger:
    def _get_client(self):
        from elasticsearch import AuthenticationException, Elasticsearch

        _client = None
        ELASTIC_USER = ""
        ELASTIC_PASSWORD = ""
        CLOUD_ID = ""

        if ELASTIC_USER and ELASTIC_PASSWORD and CLOUD_ID:
            try:
                _client = Elasticsearch(cloud_id=CLOUD_ID, basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD))
                _client.info()
            except AuthenticationException:
                _client = None
        return _client

    def _get_instance_data(self, instance):
        instance_dict = instance.__dict__.copy()
        instance_dict.pop("_instance_initialized", None)
        instance_dict.pop("_tracker", None)
        instance_dict.pop("_state", None)
        return instance_dict

    def index_model_update_log(self, instance, action):
        """Index model updated data to Elasticsearch.

        Index model updated data to Elasticsearch. It tracks the model
        changes and indexes it's updated data to an index with name
        'modelhistorylog'.

        Parameters:
        instance (obj): Model object that needed to be logged.
        action (str): Log action (update, delete, create).

        """
        if _client := self._get_client():
            can_log = True
            if action == "update":
                changes = instance.tracker.changed()
                changes.pop("updated_at")
                can_log = any(change is not None for change in changes)
            if can_log:
                index_name = instance._meta.model.__name__.lower() + "historylog"
                instance_data_dict = self._get_instance_data(instance)
                instance_data_dict.update({"timestamp": timezone.now()})
                instance_data_dict.update({"action": action})
                return _client.index(index=index_name, document=instance_data_dict)
        return None

    def index_business_log(self, index, document):
        """Index business logs to Elasticsearch.

        Index business logs to ELasticsearch. It appends
        the timestamp field to the document in order to
        track the insertion datetime.

        Parameters:
        index (str): Elasticsearch index name.
        document (obj): JSON obj represents the document data.

        """
        if _client := self._get_client():
            document.update({"timestamp": timezone.now()})
            return _client.index(index=index, document=document)
        return None
