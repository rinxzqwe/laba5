from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_create, name='recipe_create'),
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.file_list, name='file_list'),
    path('api/search/', views.search_recipes, name='search_recipes'),
    path('edit/<int:pk>/', views.edit_recipe, name='edit_recipe'),
    path('delete/<int:pk>/', views.delete_recipe, name='delete_recipe'),
]