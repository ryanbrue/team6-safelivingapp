from django.urls import path
from . import dataset_downloader
from . import views

urlpatterns = [
    path('api/update/crime', dataset_downloader.download_newest_crime_data),
    path('api/update/sortcrime', dataset_downloader.sort_crime_data_by_state),
    path('api/update/scores', dataset_downloader.refresh_crime_scores),
    path('api/update/population', dataset_downloader.fix_population_dataset),
    path('api/get/searchsuggestions/<str:currentInput>/', views.get_search_suggestions),
]