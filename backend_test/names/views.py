from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import re
from bs4 import BeautifulSoup

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
       Usage: http://localhost:3000/names
    """
    if request.method == 'GET':
        queryset = Names.objects.all()
        serializer = NamesSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        instance = Names.objects.all()
        if instance:
            instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def annotate(request):
    """
    Register url for a person
    ---
       Usage: http://localhost:3000/annotate
    """
    if request.method == 'POST':
        phrases = filter(None, re.split(r'(<a href=.+?>.+?<\/a>)', request.body))
        return_html = ''
        for phrase in phrases:
            if not re.match(r'<a href=.+?>.+?<\/a>', phrase):
                soup = BeautifulSoup(phrase, 'html.parser')
                textNodes = soup.findAll(text=True)
                for textNode in textNodes:
                    words = filter(None, re.split(r'(;|,|\'|\.|\s*)', textNode))
                    return_msg = ''
                    for word in words:
                        if not re.match(r'[;|,|\'|\.|<|>|\s*]', word):
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
                    textNode.replace_with(return_msg)
                return_html += soup.encode(formatter=None)
            else:
                return_html += phrase
        return HttpResponse(return_html, status=status.HTTP_200_OK)
