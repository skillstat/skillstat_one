from django.urls import path
from . import views

app_name = 'SkillPer'
urlpatterns = [
    path('perList/', views.per_list, name='perList'),
    path('add/', views.add_skill, name='add'),
    path('delete/', views.delete_item, name='delete'),
    path('edit/', views.edit_item, name='edit'),
    # path('test/',views.test,name='test')
]
