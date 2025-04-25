"""
URL configuration for genflow project.

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

from django.apps import apps
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if apps.is_installed("genflow.apps.team"):
    urlpatterns.append(path("api/", include("genflow.apps.team.urls")))

if apps.is_installed("genflow.apps.iam"):
    urlpatterns.append(path("api/", include("genflow.apps.iam.urls")))

if apps.is_installed("genflow.apps.core"):
    urlpatterns.append(path("", include("genflow.apps.core.urls")))

if apps.is_installed("genflow.apps.prompt"):
    urlpatterns.append(path("api/", include("genflow.apps.prompt.urls")))

if apps.is_installed("genflow.apps.assistant"):
    urlpatterns.append(path("api/", include("genflow.apps.assistant.urls")))

if apps.is_installed("genflow.apps.session"):
    urlpatterns.append(path("api/", include("genflow.apps.session.urls")))
