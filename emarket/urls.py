"""
URL configuration for emarket project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path,include,re_path
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
   openapi.Info(
      title="API Documentation",
      default_version='v1',
      description="Swagger UI for your project",
      contact=openapi.Contact(email="m7mdmonsef@gmail.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('product.urls')),
    path('api/',include('account.urls')),
    path('api/',include('order.urls')),
    
    path('api/token/', TokenObtainPairView.as_view()),
    
    path('', lambda request: HttpResponse("Welcome to the API!")),
    
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

handler404 = 'utils.error_view.handler404'
handler500 = 'utils.error_view.handler500'


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)