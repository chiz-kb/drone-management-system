"""aerobridge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path



from django.conf import settings
from django.conf.urls.static import static
import jetway.views as jetwayviews
from launchpad import views as  launchpad_views
urlpatterns = [
    path('ping/', jetwayviews.PingView.as_view(), name="ping"),
    # path('', launchpad_views.HomeView.as_view()),
    path('', jetwayviews.HomeView.as_view()),
    path('admin/', admin.site.urls),

    path('launchpad/', include('launchpad.urls')),
    path('pki/', include('pki_framework.urls')),
    path('gcs/', include('gcs_operations.urls')),
    path('registry/', include('registry.urls')),
    # YOUR PATTERNS
]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns = format_suffix_patterns(urlpatterns)