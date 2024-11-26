from django.urls import path

from .views import CreateOrListRoomsView

urlpatterns = [path("", CreateOrListRoomsView.as_view(), name="rooms")]
