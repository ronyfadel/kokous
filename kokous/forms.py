from models import User
from django import forms
from django.contrib import auth
from datetime import date, time, datetime, timedelta

class SignupForm(forms.Form):
	first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-high', 'placeholder': 'First Name'}), max_length=20)
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-high', 'placeholder': 'Last Name'}), max_length=20)
	email_address = forms.EmailField(widget=forms.TextInput(attrs={'class': 'input-high', 'placeholder': 'Email Address'}))
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-high', 'placeholder': 'Username'}), min_length=6, max_length=20)
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-high', 'placeholder': 'Password'}), min_length=6, max_length=20)
	
	def clean_username(self):
		username = self.cleaned_data['username']
		if (' ' in username or ',' in username):
			raise forms.ValidationError(u'username should not contain spaces or commas')
		
		try:
			user = User.objects.get(username=username)
			
		except User.DoesNotExist:
			return username
			
		else:
			raise forms.ValidationError(u'username %s already exists' % username )
	
class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-small', 'placeholder': 'Username'}), max_length=20)
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-small', 'placeholder': 'Password'}), max_length=20)
	
	def clean(self):
		username = self.cleaned_data.get('username', '')
		password = self.cleaned_data.get('password', '')
	
		user = auth.authenticate(username=username, password=password)
		if user is None:
			raise forms.ValidationError(u'Wrong username or password')
		if not user.is_active:
			raise forms.ValidationError(u'User is not active')
		return self.cleaned_data

valid_time_formats=["%I:%M %p", "%H:%M"]

class MeetingForm(forms.Form):
	title = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-high span8'}), max_length=255)
	description = forms.CharField(widget=forms.Textarea(attrs={'class': 'xlarge span8', 'id': 'textarea2', 'rows': '5'}))
	meeting_date = forms.DateField(initial=date.today,
									widget=forms.TextInput(attrs={'class': 'input-high span8', 'id': 'datepicker',
																'autocomplete': 'off'}))

	start_time = forms.TimeField(initial=datetime.now().time().strftime("%I:%M %p"),
								input_formats=valid_time_formats,
								widget=forms.TextInput(attrs={'class': 'input-high span8', 'id': 'inputStart',
															'autocomplete': 'off'}))

	end_time = forms.TimeField(initial=(datetime.now()+timedelta(hours=1)).time().strftime("%I:%M %p"),
										input_formats=valid_time_formats,
										widget=forms.TextInput(attrs={'class': 'input-high span8', 'id': 'inputEnd',
																'autocomplete': 'off'}))

	participants = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'input-high', 'id': 'invitedparticipants'}))
	location = forms.CharField(widget=forms.TextInput(attrs={'class': 'span8 input-high', 'id': 'locationField'}), required=False)
	
	def clean_participants(self):
		participants = self.cleaned_data['participants']
		try:
			usernames=participants.split(",")
			for username in usernames:
				user=User.objects.get(username=username)

		except User.DoesNotExist:
			raise forms.ValidationError("No such username")
		return participants
		
	def clean_end_time(self):
		start_time = self.cleaned_data['start_time']
		end_time = self.cleaned_data['end_time']
		if end_time<start_time:
			raise forms.ValidationError("End time must be greater than start time")
		return end_time

class SettingsForm(forms.Form):
	avatarFile = forms.ImageField(required=False)
	userId = forms.CharField(widget=forms.HiddenInput())
	first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'input-high'}), max_length=20)
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'input-high'}), max_length=20)
	email_address = forms.EmailField(widget=forms.TextInput(attrs={'class':'input-high'}))
	old_password = forms.CharField(required=False,widget=forms.PasswordInput(attrs={'class':'input-high','placeholder':'Old Password'}), max_length=20)
	new_password = forms.CharField(required=False,widget=forms.PasswordInput(attrs={'class':'input-high', 'placeholder':'New Password'}), max_length=20)
	bio = forms.CharField(required=False,widget=forms.Textarea(attrs={'class':'xlarge span8', 'id':'textarea2', 'rows':'5'}))
	
	def clean_old_password(self):
		userId = self.cleaned_data['userId']
		user = User.objects.get(id = int(userId))
		old_password = self.cleaned_data['old_password']
		if old_password:
			if user.check_password(self.cleaned_data['old_password']):
				return old_password
			else:
				raise forms.ValidationError(u'Wrong password')
		else:
			return old_password
			
	def clean_new_password(self):
		userId = self.cleaned_data['userId']
		user = User.objects.get(id = int(userId))
		old_password = self.cleaned_data.get('old_password', '')
		new_password = self.cleaned_data.get('new_password', '')
		if old_password:
			if not new_password:
				raise forms.ValidationError(u'Enter a new password')
			else:
				return new_password		
	
	def clean_avatarFile(self):
		avatarFile = self.cleaned_data['avatarFile']
		if avatarFile:
			max_size = 700
		
			if avatarFile.content_type != 'image/jpeg' and avatarFile.content_type != 'image/png':
				raise forms.ValidationError(
				'Image must be less a valid jpeg or png image'
				)
		
			if avatarFile.size > max_size * 1024:
				raise forms.ValidationError(
				'Image must be less then %d Kbytes.' % max_size
				)

		return avatarFile
	
class FinalizeForm(forms.Form):
	discussions = forms.CharField(widget=forms.Textarea(attrs={'class': 'xlarge span8', 'id': 'textarea2', 'rows': '6'}), required=False)
	conclusions = forms.CharField(widget=forms.Textarea(attrs={'class': 'xlarge span8', 'id': 'textarea2', 'rows': '6'}), required=False)

class ActionForm(forms.Form):
	actions = forms.CharField(widget=forms.Textarea(attrs={'class': 'xlarge span8', 'id': 'textarea2', 'rows': '6'}), required=False)
	completedActions = forms.BooleanField(required=False)
	userId = forms.CharField(widget=forms.HiddenInput(), required=False)
	name = forms.CharField(widget=forms.HiddenInput(), required=False)

class RSVPForm(forms.Form):
	RSVP_CHOICES = (
		(0, '-'),
		(1, 'Attending'),
		(2, 'Not Attending'),
		(3, 'Maybe Attending'),
	)
	rsvp_choice = forms.ChoiceField(choices=RSVP_CHOICES)

class CommentForm(forms.Form):
	text = forms.CharField(widget=forms.Textarea(attrs={'class': 'xlarge span8', 'id': 'textarea2', 'rows': '6'}))

