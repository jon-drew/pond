from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from strawberry.django.views import GraphQLView

from pond.schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', GraphQLView.as_view(schema=schema)),
    path('healthz/', lambda r: HttpResponse('ok')),
]
