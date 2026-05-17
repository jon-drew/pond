from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import GraphQLView

from pond.schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(GraphQLView.as_view(schema=schema))),
    path('healthz/', lambda r: HttpResponse('ok')),
]
