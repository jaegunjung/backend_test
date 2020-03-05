from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

class register_url(generics.ListAPIView):
   """
   Register url for a person
   ---
      Usage: http://localhost:3000/names/alex/
   """
   serializer_class = NamesSerializer
   queryset = Names.objects.all()
   filter_fields = '__all__'

   def get_queryset(self):
       """
       Reads name from request and updates the querset
       :return: New queryset with name
       """
       name = self.kwargs['name']
       queryset = self.queryset.filter(name=name)
       return queryset
