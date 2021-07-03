from django.urls import path
from api.views import NFLRushingView, NFLRushingEXCLView

urlpatterns = [
    path('listStats/', NFLRushingView.as_view(), name='list-stats'),
    path('listStatsExcel/', NFLRushingEXCLView.as_view(), name='list-stats-excel'),
]
