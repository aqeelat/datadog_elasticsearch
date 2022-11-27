# Datadog Elasticsearch Bug Demo

To demonstrate the issue:
1. run `ddtrace-run python manage.py runserver`
2. open http://localhost:8000/

To demonstrate the workaround:
1. run `DD_TRACE_ELASTICSEARCH_ENABLED=false ddtrace-run python manage.py runserver`
2. open http://localhost:8000/
