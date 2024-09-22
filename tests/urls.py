from django.urls import path

from .views import start_test_session, completed_test_session

urlpatterns = [
    path('start/', start_test_session, name='start-test-session'),
    path('completed/', completed_test_session, name='completed-test-session'),
]
