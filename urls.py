from django.conf.urls.defaults import patterns, include, url
from kokous.views import generalViews, profileViews, meetingViews, apiViews, miscViews

#enables admin
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	
	# Kokous Views
	# General Views
	url(r'^$', generalViews.home),
	url(r'^signup/$', generalViews.signup),
	url(r'^login/$', generalViews.login),
	url(r'^logout/$', generalViews.logout),
	
	# Profile Views
	url(r'^profile/$', profileViews.profile),
	url(r'^user/(\d*)$', profileViews.user),
	url(r'^settings/$', profileViews.settings),
	
	# Meeting Views
	url(r'^meetings/$', meetingViews.meetings),
	url(r'^meeting/(\d*)$', meetingViews.viewMeeting),
	url(r'^meeting/create/$', meetingViews.createMeeting),
	url(r'^meeting/edit/(\d*)$', meetingViews.editMeeting),
	url(r'^meeting/finalize/(\d*)$', meetingViews.finalizeMeeting),
	url(r'^meeting/rsvp/(\d*)$', meetingViews.rsvpMeeting),
	url(r'^meeting/comment/create/(\d*)$', meetingViews.createComment),

	# API Views
	url(r'^api/([a-z]*).json$', apiViews.api),

	# Misc Views
	url(r'^about/', miscViews.misc),
	url(r'^blog/', miscViews.misc),
	url(r'^contact/', miscViews.misc),
	url(r'^TOS/', miscViews.misc),
	url(r'^resources/', miscViews.misc),
	url(r'^privacy/', miscViews.misc),
	
	# Admin
    url(r'^admin/', include(admin.site.urls)),
)


import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
)