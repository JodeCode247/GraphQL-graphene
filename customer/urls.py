from django.urls import path,include
from . import views 

app_name = "client"

urlpatterns = [
    
    path('',views.index,name='home'),
    path('submit-quiz/',views.submit_quiz,name='submit'),
]