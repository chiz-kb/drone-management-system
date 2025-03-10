from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns


from django.conf import settings
from django.conf.urls.static import static
import jetway.views as jetwayviews
from launchpad import views as  launchpad_views


urlpatterns = [
    path('ping/', jetwayviews.PingView.as_view(), name="ping"),
    # path('', launchpad_views.HomeView.as_view()),
    path('', jetwayviews.HomeView.as_view()),
    path('',jetwayviews.HomeView.as_view(),name='home'),
    path('home',jetwayviews.HomeView.as_view()),
    path('index', jetwayviews.index,name='index'),
    path("login", jetwayviews.login, name="login"),
    path("logout", jetwayviews.logout, name="logout"),
    path("callback", jetwayviews.callback, name="callback"),
    path('admin/', admin.site.urls),

    path('launchpad/', include('launchpad.urls')),
    path('pki/', include('pki_framework.urls')),
    path('gcs/', include('gcs_operations.urls')),
    path('registry/', include('registry.urls')),
    # YOUR PATTERNS
]

urlpatterns = [
    *i18n_patterns(*urlpatterns, prefix_default_language=True),
    path("set_language/<str:language>", launchpad_views.set_language, name="set-language"),
]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns = format_suffix_patterns(urlpatterns)