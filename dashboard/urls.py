from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('pages/', views.pages_list, name='pages_list'),
    path('pages/create/', views.page_create, name='page_create'),
    path('pages/<int:page_id>/builder/', views.page_builder, name='page_builder'),
    path('pages/<int:page_id>/publish/', views.publish_page, name='publish_page'),
    path('pages/<int:page_id>/discard/', views.discard_drafts, name='discard_drafts'),
    path('sections/<int:section_id>/edit/', views.section_edit, name='section_edit'),
    path('sections/<int:section_id>/delete/', views.section_delete, name='section_delete'),
    path('sections/<int:section_id>/toggle/', views.section_toggle, name='section_toggle'),
    path('sections/<int:section_id>/move/<str:direction>/', views.section_move, name='section_move'),
    path('pages/<int:page_id>/sections/add/', views.section_add, name='section_add'),
    path('upload-image/', views.upload_image, name='upload_image'),
    path('gallery-images/', views.gallery_images, name='gallery_images'),
]

