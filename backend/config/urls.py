from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    # ルートディレクトリにアクセスした場合は、admin.urlsにリダイレクトする
    path('', RedirectView.as_view(url='admin/', permanent=True)),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls'), name='api'),
]
