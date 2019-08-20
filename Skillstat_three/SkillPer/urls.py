from django.urls import path
from . import views

app_name = 'SkillPer'
urlpatterns = [
    path('add/', views.add_skill, name='add'),
    path('delete/', views.delete_item, name='delete'),
    path('edit/', views.edit_item, name='edit'),
    path('contrast/', views.contrast, name='contrast'),
    path('list/', views.SkillListView.as_view(), name='list')
    # path('test/', views.test, name='test')
]
