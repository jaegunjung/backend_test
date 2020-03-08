from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import re

from models import Names
from serializers import NamesSerializer


@api_view(['GET', 'PUT', 'DELETE'])
def register_url(request, name):
    """
    Register url for a person
    ---
       Usage: http://localhost:3000/names/alex
    """
    if request.method == 'GET':
        queryset = Names.objects.all()
        queryset = queryset.filter(name=name)
        if queryset:
            serializer = NamesSerializer(queryset, many=True)
            return Response(serializer.data[0])
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'PUT':
        request.data['name'] = name
        try:
            queryset = Names.objects.get(name=name)
        except Names.DoesNotExist:
            queryset = None
        if queryset:
            serializer = NamesSerializer(queryset, data=request.data)
        else:
            serializer = NamesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        instance = Names.objects.get(name=name)
        if instance:
            instance.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'DELETE'])
def register_url_all(request):
    """
    Register url for all
    ---
       Usage: http://localhost:3000/names/
    """
    if request.method == 'GET':
        queryset = Names.objects.all()
        serializer = NamesSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        instance = Names.objects.all()
        # print 'instance'
        # print instance
        if instance:
            instance.delete()
        return Response([], status=status.HTTP_200_OK)


@api_view(['POST'])
def annotate(request):
    """
    Register url for a person
    ---
       Usage: http://localhost:3000/annotate
    """
    if request.method == 'POST':
        return_msg = ""
        # words = request.body.split()
        # words = re.split(r'(;|,|\s)\s*', request.body)
        print '-1', request.body
        # phrases0 = filter(None, re.split(r'(<a href=.+?>.+?<\/a>)', request.body))
        phrases0 = filter(None, re.split(r'(<a href=.+?>.+?<\/a>|<div class=.+?>)', request.body))
        for phrase0 in phrases0:
            print '0', phrase0
            if not re.match(r'<a href=.+?>.+?<\/a>|<div class=.+?>', phrase0):
                # phrases = filter(None, re.split(r'(?<=>)(.+?)(?=<)', phrase0))
                phrases = filter(None, re.split(r'(<.+?>)', phrase0))
                for phrase in phrases:
                    print '0.5', phrase
                    if not re.match(r'<.+?>', phrase):
                        # words = filter(None, re.split(r'(;|,|\'|\.|\s*)', phrase))
                        words = filter(None, re.split(r'(;|,|\'|\.|<|>|\s*)', phrase))
                        print '0.7', words
                        for i, word in enumerate(words):
                            print '1', word
                            # if not re.match(r'[;|,|\'|\.|\s*]', word):
                            if not re.match(r'[;|,|\'|\.|<|>|\s*]', word):
                                print '2', word
                                try:
                                    queryset = Names.objects.get(name=word)
                                except Names.DoesNotExist:
                                    queryset = None
                                if queryset:
                                    url = Names.objects.values_list('url', flat=True).get(name=word)
                                    return_msg = return_msg + '<a href="' + url + '">' + word + '</a>'
                                else:
                                    return_msg += word
                            else:
                                return_msg += word
                    else:
                        return_msg += phrase
            else:
                return_msg += phrase0
        return HttpResponse(return_msg, status=status.HTTP_200_OK)
