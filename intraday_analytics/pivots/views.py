from django.shortcuts import render
from django.http import HttpResponse
from .strategy.data.push_db import intraday_tasks, eod_tasks


def index(request):
    return render(request, 'pivots/index.html', {})
