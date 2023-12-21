from django.urls import path, include

from  .views import question, qiuz, result_list, ResultView, login_view, logout_view

urlpatterns = [
    path('', qiuz, name='qiuz'),
    path('quiz/<int:pk>/', question, name='quistion'),
    path('results/', ResultView.as_view(), name='results'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout')
]