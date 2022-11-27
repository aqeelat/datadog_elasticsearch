from django.utils import timezone


class Logger:

    _client = None

    @property
    def client(self):
        if not self._client:

            from elasticsearch import AuthenticationException, Elasticsearch

            _client = None
            username = ""
            password = ""
            cloud_id = ""

            if username and password and cloud_id:
                try:
                    _client = Elasticsearch(cloud_id=cloud_id, basic_auth=(username, password))
                    _client.info()
                except AuthenticationException:
                    _client = None
            self._client = _client
        return self._client

    def index_business_log(self, index, document):
        """Index business logs to Elasticsearch.

        Index business logs to ELasticsearch. It appends
        the timestamp field to the document in order to
        track the insertion datetime.

        Parameters:
        index (str): Elasticsearch index name.
        document (obj): JSON obj represents the document data.

        """
        if _client := self.client:
            document.update({"timestamp": timezone.now()})
            return _client.index(index=index, document=document)
        return None
