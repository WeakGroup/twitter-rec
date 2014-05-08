from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'website.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'website.views.home'),
    url(r'^recommend/', 'website.views.recommend'),
    url( r'\.(jpeg|css|js|png|PNG|jpg|JPEG|JPG|gif|GIF|xml|swf|html)$', 'website.views.get_file'),
    url(r'^admin/', include(admin.site.urls)),
)
