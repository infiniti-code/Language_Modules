from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.templatetags.static import static

#import json
from .models import search
#from analysis_summarization.settings import *
from rest_framework.views import APIView
from language_modules.settings import *
from django.views.decorators.csrf import csrf_exempt
from analysis_summarization.analysis import analysis_plot, analysis_plot_fixed_data
import matplotlib.pyplot as plt
#from analysis_summarization.tech_nonTech import final


# Create your views here.
global query
def tag_search(request):
    if request.method == 'GET':
        query = request.GET.get('tag')
        sizes = analysis_plot(query)
        labels = 'Negative', 'Positive', 'Neutral'

        explode = (0, 0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        fig1.savefig("C:\\Users\\Praful\\Desktop\\My_Django_Stuff\\language_modules\\analysis_summarization\\plots_analysis\\{0}.png".format(query), delimiter=",")
        plt.show()
        url = {'url': 'http://localhost:8000/static/'+query+'.png'}

        return JsonResponse(url)

def tag_search_static(request):
    if request.method == 'GET':
        query = request.GET.get('tag')
        labels = 'Negative', 'Positive', 'Neutral'
        sizes = analysis_plot_fixed_data(query)
        explode = (0, 0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        fig1.savefig("C:\\Users\\Praful\\Desktop\\My_Django_Stuff\\language_modules\\analysis_summarization\\plots_analysis\\airline.png", delimiter=",")
        url = {'url': 'http://localhost:8000/static/airline.png'}
        plt.show()
        return JsonResponse(url)





'''
class PhotoDetail(APIView):

    #permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get_object(self, pk):
        try:
            return MyPhoto.objects.get(pk=1)
        except MyPhoto.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        photo = self.get_object(pk)
        serializer = PhotoSerializer(photo)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        photo = self.get_object(pk)
        serializer = PhotoSerializer(photo, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        photo = self.get_object(pk)
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def pre_save(self, obj):
        obj.owner = self.request.user
'''
