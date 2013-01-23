from django.contrib import admin
from kokous.models import UserProfile, UserOAuth, Meeting, UserMeeting

# date_hierarchy = 'created_date_time'

class MeetingAdmin(admin.ModelAdmin):
	list_display = ('title', 'description', 'location', 'created_date_time', 'meeting_date', 'start_time')
	search_fields = ('title',)
	ordering = ('created_date_time',)

class UserMeetingAdmin(admin.ModelAdmin):
	list_display = ('user', 'meeting', 'is_Admin', 'actions')
	search_fields = ('user', 'meeting',)
	ordering = ('user',)


admin.site.register(UserProfile)
admin.site.register(UserOAuth)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(UserMeeting, UserMeetingAdmin)