from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from django.views import generic

class Example1(generic.TemplateView):
    template_name = "examples/example_1.html"

class Example2(generic.TemplateView):
    template_name = "examples/example_2.html"

class Example3(generic.TemplateView):
    template_name = "examples/example_3.html"

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'example.views.home', name='home'),
    # url(r'^example/', include('example.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^example1/$', Example1.as_view()),
    url(r'^example2/$', Example2.as_view()),
    url(r'^example3/$', Example3.as_view()),
)
