from rest_framework.decorators import api_view
from rest_framework.response import Response
from celery import shared_task
@api_view(['GET','POST'])
def post_tasks(request):
    items=request.data
    print(items)
    if isinstance(items,list):
        return Response({'message':'correct'})
    else:
        return Response({'message':'correct'})
    
    
    
    
    # Create your views here.
