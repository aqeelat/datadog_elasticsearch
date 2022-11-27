from django.http import HttpResponse
from mixins.logging import Logger


# Create your views here.
def detail(request):
    Logger().index_business_log(index="test", document={"message": "test_message"})
    return HttpResponse("Hello DataDog")
