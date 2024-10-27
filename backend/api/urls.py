from django.urls import path
from .views import TouchDataView

urlpatterns = [
    path('api/touches/<int:match_id>/<str:player_name>/', TouchDataView.as_view(), name='touch-data')
]
