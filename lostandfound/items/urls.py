from django.urls import path
from . import views
from .views import signup_view
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('', views.index, name='index'),
    path('report/', views.report, name='report'),
    path('items/', views.items_list, name='items'),
    path('item/<uuid:item_id>/', views.item_detail, name='item_detail') ,
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout') ,
    path('report/', views.ReportedItem, name='report_item'),
    path('thank-you/', views.thank_you, name='thank_you'), 

]
