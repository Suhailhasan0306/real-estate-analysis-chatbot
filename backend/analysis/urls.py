from django.urls import path
from .views import analyze_query

urlpatterns = [
    path('analyze/', analyze_query, name='analyze-query'),
]
