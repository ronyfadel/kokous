from __init__ import *

#meeting: meeting_date, start_time, end_time
def profile(request):
	if not request.user.is_authenticated():
		return HttpResponseForbidden("<h1>Forbidden</h1><p>user not authenticated</p>")
	
	# Meetings Today
	todayDate = date.today() # today
	now = datetime.now() # now
	notifications = Meeting.objects.filter( Q(meeting_date=todayDate), Q(members=request.user), Q(start_time__gt=now) )

	# New Meetings -> (Created between yesterday and today AND are not done), or user was not notified
	yesterdayDate = date.today() + timedelta(days=-2)
	
	newMeetings = []
	todayDate = date.today() + timedelta(days=+1) # today
	for userMeeting in request.user.usermeeting_set.filter( Q(notified=False) | Q(meeting__created_date_time__range=(yesterdayDate, todayDate)),
															Q(meeting__meeting_date__gt=todayDate) ):
		if userMeeting.notified == False:
			userMeeting.notified = True
			userMeeting.save()
		newMeetings.append(userMeeting.meeting)
	
	print newMeetings
	
	actions = UserMeeting.objects.filter( Q(completedActions=False), Q(user=request.user) ).exclude(actions='')
	
	sectionTitle = inspect.stack()[0][3]
	c={'sectionTitle': sectionTitle, 'sections': sections, 'notifications': notifications, 'newMeetings': newMeetings, 'actions': actions}
	return render_to_response('%s.html' % sectionTitle, c, context_instance=RequestContext(request))

def user(request, id):
	if not request.user.is_authenticated():
		return HttpResponseForbidden("<h1>Forbidden</h1><p>user not authenticated</p>")
	try:
		visitedUser = User.objects.get(id=id)

	except User.DoesNotExist:
		raise Http404

	else:
		if visitedUser == request.user:
			return HttpResponseRedirect('/profile/')
		
		meetings = []
		for meeting in visitedUser.meeting_set.all():
			try:
				print request.user
				UserMeeting.objects.get(user=request.user, meeting=meeting)

			except UserMeeting.DoesNotExist:
				pass

			else:
				meetings.append(meeting)
				
		c={}
		c.update({'sections' : sections, 'visitedUser': visitedUser, 'meetings' : meetings})
		return render_to_response('user.html', c, context_instance=RequestContext(request))

from hashlib import sha1
import os
from settings import MEDIA_ROOT
import Image, ImageOps
hashSalt = '$!@#%@$^#$'
from django.core.files import File

def settings(request):
	if not request.user.is_authenticated():
		return HttpResponseForbidden("<h1>Forbidden</h1><p>user not authenticated</p>")
	
	c={}
	c.update(csrf(request))
	
	if request.method == 'POST':
		settingsForm = SettingsForm(request.POST, request.FILES)
		if settingsForm.is_valid():
			avatarFile = settingsForm.cleaned_data['avatarFile']
			if avatarFile:
				userProfile = UserProfile.objects.get(user=request.user)
				if userProfile.avatar:
					userProfile.avatar.delete(save=False) # deleting old avatar
				# creating new one, with sha1'ed name
				hashingFunc = sha1()
				hashingFunc.update(hashSalt + str(request.user.id))
				avatarFileName = "%s.%s" % (hashingFunc.hexdigest(), avatarFile.content_type.split('/')[1])
				
				originalImage = Image.open(avatarFile)
				resizedImage = ImageOps.fit(originalImage, (300, 300), Image.ANTIALIAS)
				
				tmpDest = os.path.join(MEDIA_ROOT, 'avatars', 'tmp' + avatarFileName)
				resizedImage.save(tmpDest)
				f = open(tmpDest)
				avatarResizedFile = File(f)
				userProfile.avatar.save(avatarFileName, avatarResizedFile)
				avatarResizedFile.close()
				os.remove(tmpDest)
		########
			user = request.user
			user.first_name = settingsForm.cleaned_data['first_name']
			user.last_name = settingsForm.cleaned_data['last_name']
			user.email = settingsForm.cleaned_data['email_address']
			user.userprofile.bio = settingsForm.cleaned_data['bio']
			if settingsForm.cleaned_data['old_password']:
				if settingsForm.cleaned_data['new_password']:
					user.set_password(settingsForm.cleaned_data['new_password'])
			user.save()
			user.userprofile.save()

			return HttpResponseRedirect('/settings/')

	else:
		settingsForm = SettingsForm(
				{
					'userId': str(request.user.id),
					'first_name':request.user.first_name,
					'last_name':request.user.last_name,
					'email_address':request.user.email,
					'bio' :request.user.userprofile.bio
				})

	sectionTitle = inspect.stack()[0][3]
	c.update({'sectionTitle' : sectionTitle, 'sections' : sections, 'settingsForm': settingsForm})
	return render_to_response('%s.html' % sectionTitle, c, context_instance=RequestContext(request))
	
	
	