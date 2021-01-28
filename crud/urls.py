from django.urls import path
from . import views
#from django.contrib.auth.views import LoginView, LogoutView

app_name = 'crud'


urlpatterns = [
    #path('signin/', LoginView.as_view(template_name='crud/signin.html'), name='signin'),
    path('signin/', views.sign_in, name='signin'),
    path('signup/', views.sign_up, name='signup'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name="profile"),
    #path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('logout/', views.log_out, name='logout'),
    path('', views.home, name='home')

]

