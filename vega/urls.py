from django.conf.urls import url,include,patterns
import settings
from . import view


urlpatterns = patterns('',
                       url(r'^main$', view.main),
                       #url(r'^index$', view.index),
                       url(r'^app_tower/', include('app_tower.urls')),
                       url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_URL}),
)
