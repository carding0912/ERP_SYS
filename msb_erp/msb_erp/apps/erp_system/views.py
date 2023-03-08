import logging

from django.shortcuts import render
from rest_framework.response import Response

# Create your views here.
from rest_framework.views import APIView

logger = logging.getLogger('erp')
class Hello(APIView):
    """
    测试视图,以及logging日志
    """
    def get(self,request):
        logger.debug('debug基本的日志')
        logger.info('info基本的日志')
        logger.error('error级别的日志')
        return Response({'message':'Test OK'})