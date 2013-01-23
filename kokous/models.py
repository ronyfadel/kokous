from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):  
	user = models.OneToOneField(User)
	bio = models.TextField(blank=True)
	avatar = models.ImageField(blank=True, upload_to='avatars/')
	
	def __unicode__(self):
		return self.user.username

class UserOAuth(models.Model):
	user = models.OneToOneField(User)
	OAuthKey = models.CharField(max_length=40)

class Meeting(models.Model):
	members = models.ManyToManyField(User, through='UserMeeting')
	title = models.CharField(max_length=255)
	description = models.TextField()
	discussions = models.TextField(blank=True)
	conclusions = models.TextField(blank=True)
	created_date_time = models.DateTimeField()
	meeting_date = models.DateField()
	start_time = models.TimeField()
	end_time = models.TimeField()
	location = models.CharField(max_length=255, blank=True)
	
	def __unicode__(self):
		return self.title
		
	class Meta:
		ordering = ['-meeting_date', 'start_time']

class UserMeeting(models.Model):
	user = models.ForeignKey(User)
	meeting = models.ForeignKey(Meeting)
	is_Admin = models.BooleanField()
	actions = models.TextField(blank=True)
	notified = models.BooleanField(default=False)
	completedActions = models.BooleanField(default=False)
	RSVP_CHOICES = (
		(0, 'Has not replied'),
		(1, 'Attending'),
		(2, 'Not Attending'),
		(3, 'Maybe Attending'),
	)
	rsvp_status = models.IntegerField(choices=RSVP_CHOICES, default=0)

class Comment(models.Model):
	user = models.ForeignKey(User)
	meeting = models.ForeignKey(Meeting)
	text = models.TextField()
	created_date_time = models.DateTimeField()

	class Meta:
		ordering = ['created_date_time']