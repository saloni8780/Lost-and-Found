from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup_view, name='signup'),  
    #path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
     path('find/', views.find_item, name='find_item'),
    path('post/', views.post_item_view, name='post_item'),
    path('about/', views.about_us, name='about_us'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('delete-item/<int:item_id>/', views.delete_item, name='delete_item'),
    

]
