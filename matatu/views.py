from django.shortcuts import render
from matatu import models as app_models
from django.shortcuts import render
import plotly.graph_objects as go
from plotly.offline import plot
import plotly,json
import pandas as pd
from .src.twitter_handler import search_action
import json, random
from django.http import JsonResponse
from django.db.models import Q
from django.views.generic import TemplateView
from django.http import HttpResponse,HttpResponseRedirect
from django.core import serializers 


# Create your views here.


def tweet_table(request):
    if request.method == 'GET':
       query = request.GET.get('q')
       if query is not None:
           lookups = Q(route__icontains=query) | Q(conditions__icontains=query) | Q(date__icontains=query)
           gotten = app_models.TweetObject.objects.filter(lookups).distinct()
           tweets = []
           for t in gotten:
                if t.route is not None:
                   tweets.append(t)
           return render(request,'matatu_templates/tweet_table.html',{'results':tweets,'query':query})
    results = []
    tweets = app_models.TweetObject.objects.order_by('created_date').reverse()
    for t in tweets:
        if t.route is not None:
            results.append(t)
    return render(request,'matatu_templates/tweet_table.html',{'results':results})


def pie_chart(request):
    def scatter():
        accident_tweets = app_models.TweetObject.objects.filter(conditions ="accident")
        traffic_tweets = app_models.TweetObject.objects.filter(conditions ="traffic")
        police_activty_tweets = app_models.TweetObject.objects.filter(conditions ="police")
        roadblock_tweets = app_models.TweetObject.objects.filter(conditions ="road block")
        labels = ['Accident', 'Traffic', 'Police_Activity', 'Roadblock']
        values = [accident_tweets.count(),traffic_tweets.count(),police_activty_tweets.count(),roadblock_tweets.count()]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        plot_div = plot(fig, include_plotlyjs=False, output_type='div')
        return plot_div
    context = {"plot": scatter()}

    return render(request, 'matatu_templates/charts.html', context)

def graph(request):
    def scatter():
        months = ['Huruma', 'Thika Road', 'Mombasa Road','Langata Road','Githurai','Ngong Road','Roysambu','Eastern Bypass','Outering','Uhuru Highway', 'Highrise', 'Buruburu',
                  'CBD', 'Kawangware', 'Embakasi', 'babadogo', 'rongai', 'Kangemi','Kenyatta Avenue']

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=months,
            y=[get_data('huruma'), get_data('thika road'), get_data('mombasa road'),get_data('langata road'),get_data('githurai'),get_data('ngong road'),get_data('roysambu'),get_data('eastern bypass'),get_data('outering'),get_data('uhuru'), get_data('highrise'),
               get_data('buruburu'),
               get_data('cbd'), get_data('kawangware'), get_data('embakasi'), get_data('babadogo'), get_data('rongai'),
               get_data('kangemi'),get_data('kenyatta')],
            name='Primary Product',
            marker_color='indianred'
        ))
        # fig.add_trace(go.Bar(
        #     x=months,
        #     y=[19, 14, 22, 14, 16, 19, 15, 14, 10, 12, 12, 16],
        #     name='Secondary Product',
        #     marker_color='lightsalmon'
        # ))
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(barmode='group', xaxis_tickangle=-45)
        plot_div = plot(fig, include_plotlyjs=False, output_type='div')
        return plot_div

    context = {"plot": scatter()}
    return render(request, 'matatu_templates/graph.html', context)

def get_data(value):
    tweets = app_models.TweetObject.objects.filter(route=value).count()
    return tweets

def raw_tweets(request):
    if request.method == 'GET':
       query = request.GET.get('q')
       if query is not None:
           lookups = Q(route__icontains=query) | Q(conditions__icontains=query) | Q(date__icontains=query)
           results = app_models.TweetObject.objects.filter(lookups).distinct()
           return render(request,'matatu_templates/raw_tweets.html',{'raw_tweets' : results})
    tweets = app_models.TweetObject.objects.order_by('created_date')
    return render(request,'matatu_templates/raw_tweets.html',{'raw_tweets':tweets})


def conditions(route,value):
    tweets = app_models.TweetObject.objects.filter(route = route ).filter(conditions = value)
    return tweets


def scatter(condition):
    months = ['Huruma', 'Thika Road', 'Mombasa Road','Ngong Road','Langata Road','Eastern Bypass','Outering','Uhuru Highway', 'Highrise', 'Buruburu',
                  'CBD', 'Kawangware', 'Embakasi', 'babadogo', 'rongai', 'Kangemi','Kenyatta','Kangundo Road']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=months,
            y=[conditions('huruma',condition).count(), conditions('thika road',condition).count(), conditions('mombasa road',condition).count(),conditions('ngong road',condition).count(),conditions('langata road',condition).count(),conditions('eastern bypass',condition).count(),3,conditions('uhuru',condition).count(), conditions('highrise',condition).count(),conditions('buruburu',condition).count(),
               conditions('cbd',condition).count(), conditions('kawangware',condition).count(), conditions('embakasi',condition).count(), conditions('babadogo',condition).count(), conditions('rongai',condition).count(),
               conditions('kangemi',condition).count(),conditions('kenyatta',condition).count(),3],
            name='Primary Product',
               marker_color='indianred'
        ))
    fig.update_layout(barmode='group', xaxis_tickangle=-45)
    plot_div = plot(fig, include_plotlyjs=False, output_type='div')
    return plot_div       

def graph_condition(request):
    context ={'accident' : scatter("accident"),
             'traffic' : scatter('traffic'),
             'police' : scatter('police'),
             'roadblock':scatter('road block')}
    return render(request,'matatu_templates/conditions.html',context)


def sentiments(request):
    polarity = []
    route = []
    sentiment  = app_models.TweetObject.objects.values('polarity','route')
    for s in sentiment:
        if s['route'] is not None:
            if s['route']  not in route:
                route.append(s['route'])
                polarity.append(s['polarity'])
    context = {
        'route': route,
        'polarity': polarity}
    return render(request,'matatu_templates/sentiments.html',context)

def police_sentiment(request):
    route = []
    polarity = []
    police = app_models.TweetObject.objects.values('route','conditions','polarity')
    for p in police:
        if p['conditions'] == "police":
            if p['route'] is not None:
                if p['route']  not in route:
                    route.append(p['route'])
                    polarity.append(p['polarity'])
    context = {
        'route': route,
        'polarity': polarity}
    return render(request,'matatu_templates/police_sentiment.html',context)

def positive_tweets(request):
    if request.method == 'GET':
       query = request.GET.get('q')
       if query is not None:
           lookups = Q(route__icontains=query) | Q(conditions__icontains=query) | Q(date__icontains=query)
           results = app_models.TweetObject.objects.filter(polarity__gte = 0.1).filter(lookups).distinct()
           return render(request,'matatu_templates/positive_tweets.html',{'positive_tweets' : results})
    tweets = app_models.TweetObject.objects.order_by('created_date').filter(polarity__gte = 0.1)
    return render(request,'matatu_templates/positive_tweets.html',{'positive_tweets':tweets})

def negative_tweets(request):
    if request.method == 'GET':
       query = request.GET.get('q')
       if query is not None:
           lookups = Q(route__icontains=query) | Q(conditions__icontains=query) | Q(date__icontains=query)
           results = app_models.TweetObject.objects.filter(polarity__lte = -0.2).filter(lookups).distinct()
           return render(request,'matatu_templates/negative_tweets.html',{'negative_tweets' : results})
    tweets = app_models.TweetObject.objects.order_by('created_date').filter(polarity__lte = -0.2)
    return render(request,'matatu_templates/negative_tweets.html',{'negative_tweets':tweets})

def reload_tweets(request):
    search_action.insert()
    return HttpResponseRedirect (request.path_info)


def mapCoordinates(request):
    '''
    get coordinates from db
    get any other information from db
    json encode all the data
    '''
    data  = app_models.TweetObject.objects.filter(latitude__isnull = False).reverse()
    alldata = []
    u = 1
    for i in data:
        lats = ["lat", "long","conditions","route","count"]
        coords = [i.latitude,i.longitude, i.conditions,i.route,u]
        u+=1
        zipped = zip(lats,coords)
        alldata.append(dict(zipped))
    print(alldata)
    return render(request, "matatu_templates/map.html", {"data":json.dumps(alldata)})


def mapping(request):
    data = mapCoordinates(request)
    return render(request, "matatu_templates/map.html", {"data":data})


    
# heatmap coordinates
def heatmap(request):
    '''
    get data to be used in the heat map from db
    json encode all the data
    '''
    data  = app_models.TweetObject.objects.filter(latitude__isnull=False).filter(conditions="construction")
    alldata = []
    u = 1
    for i in data:
        lats = ["lat", "long","count"]
        coords = [i.latitude,i.longitude, u]
        u+=1
        zipped = zip(lats,coords)
        alldata.append(dict(zipped))
    # data = serializers.serialize('json', data)
    return render(request, "matatu_templates/construction.html", {"data":json.dumps(alldata)})

    # return JsonResponse(json.loads(json.dumps(alldata)), safe=False) 

def heating(request):
    data = heatmap(request)
    return render(request, "matatu_templates/construction.html", {"data":data})