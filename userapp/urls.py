from django.conf.urls import url,include
from .views import LoginView, RegisterView,LogoutView
urlpatterns = [
    url(r'^login/', LoginView.as_view(),name='login'),
    url(r'^register/', RegisterView.as_view(), name='register'),
    url(r'^logout/', LogoutView.as_view(), name='lougot'),

]
