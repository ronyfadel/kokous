from __init__ import *

def createMeeting(request):
	if not request.user.is_authenticated():
		return HttpResponseForbidden("<h1>Forbidden</h1><p>user not authenticated</p>")

	c={}
	c.update(csrf(request))
	if request.method == 'POST':
		meetingForm = MeetingForm(request.POST)
		if meetingForm.is_valid():
			membersText=meetingForm.cleaned_data['participants']

			users=[request.user]
			usernames=membersText.split(",")
			for username in usernames:
				user=User.objects.get(username=username)
				users.append(user)
				
			meeting = Meeting.objects.create(title=meetingForm.cleaned_data['title'], 
											description=meetingForm.cleaned_data['description'], 
											created_date_time=datetime.now(), 
											meeting_date=meetingForm.cleaned_data['meeting_date'],
											start_time=meetingForm.cleaned_data['start_time'],
											end_time=meetingForm.cleaned_data['end_time'],
											location=meetingForm.cleaned_data['location'])
			for user in users:
				if user is request.user:
					userMeeting = UserMeeting(user=user,
											meeting=meeting,
											is_Admin=True)
				else:
					userMeeting = UserMeeting(user=user,
											meeting=meeting,
											is_Admin=False)
				userMeeting.save()
			return HttpResponseRedirect("/meetings/")

	else:
		meetingForm = MeetingForm()

	c.update({'meetingForm': meetingForm, 'sections': sections, 'sectionTitle': 'Create Meeting'})
	return render_to_response('createMeeting.html', c, context_instance=RequestContext(request))

def meetings(request):
	if not request.user.is_authenticated():
		return HttpResponseForbidden("<h1>Forbidden</h1><p>user not authenticated</p>")
	
	meetings = request.user.meeting_set.all()	
	c={}
	c.update({'sectionTitle': inspect.stack()[0][3], 'sections': sections, 'meetings': meetings})
	return render_to_response('meetings.html', c, context_instance=RequestContext(request))

def viewMeeting(request, meetingId):
	if not request.user.is_authenticated():
		return HttpResponseForbidden("<h1>Forbidden</h1><p>user not authenticated</p>")
	
	try:
		meeting = Meeting.objects.get(id=meetingId)
		
	except Meeting.DoesNotExist:
		raise Http404
		
	else:
		try:
			userMeeting = UserMeeting.objects.get(user=request.user, meeting=meeting)

		except UserMeeting.DoesNotExist:
			return HttpResponseForbidden("<h1>Forbidden</h1><p>user not authenticated</p>")

		else:					
			c={}
			c.update(csrf(request))
			c.update({'meeting': meeting, 'isAdmin': userMeeting.is_Admin,
					'userMeetings': UserMeeting.objects.filter(meeting=meeting),
					'rsvpForm': RSVPForm(initial={'rsvp_choice': userMeeting.rsvp_status}),
					'commentForm': CommentForm(), 'sections': sections})
			
			rsvp_choices = ['haveNotRepliedMembersUserMeetings', 'attendingMembersUserMeetings',
							'maybeAttendingMembersUserMeetings', 'notAttendingMembersUserMeetings']
			for index, choice in enumerate(rsvp_choices):
				c.update( {choice: UserMeeting.objects.filter(meeting=meeting, rsvp_status=index)} )
			
			return render_to_response('meeting.html', c, context_instance=RequestContext(request))

def editMeeting(request, meetingId):
	try:
		meeting = Meeting.objects.get(id=meetingId)
		
	except Meeting.DoesNotExist:
		raise Http404

	try:
		userMeeting = UserMeeting.objects.get(user=request.user, meeting=meeting)

	except UserMeeting.DoesNotExist:
		return HttpResponseForbidden("<h1>Forbidden</h1><p>user not authenticated</p>")
	
	if not userMeeting.is_Admin:
		return HttpResponseForbidden("<h1>Forbidden</h1><p>user is not admin to meeting</p>")
		
	if request.method != 'POST':
		participants = []
		for member in meeting.members.all():
			if member != request.user:
				participants.append(member.username)
		
		meetingForm = MeetingForm(initial={'title': meeting.title, 'meeting_date': meeting.meeting_date,
											'start_time': meeting.start_time.strftime("%I:%M %p"), 'end_time': meeting.end_time.strftime("%I:%M %p"),
											'participants': ','.join(participants), 'location': meeting.location,
											'description': meeting.description})
											
	else:
		meetingForm = MeetingForm(request.POST)
		if meetingForm.is_valid():
			membersText=meetingForm.cleaned_data['participants']

			newUsers=[request.user]
			usernames=membersText.split(",")
			for username in usernames:
				user=User.objects.get(username=username)
				newUsers.append(user)

			meeting.title=meetingForm.cleaned_data['title']
			meeting.description=meetingForm.cleaned_data['description']
			meeting.meeting_date=meetingForm.cleaned_data['meeting_date']
			meeting.start_time=meetingForm.cleaned_data['start_time']
			meeting.end_time=meetingForm.cleaned_data['end_time']
			meeting.location=meetingForm.cleaned_data['location']

			meeting.save()
		
			# Deleting old users that were in the meeting, and are now removed
			oldUsers = []
			for userMeeting in UserMeeting.objects.filter(meeting=meeting):
				oldUsers.append(userMeeting.user)
			
			indexesToDelete = []
			for index, oldUser in enumerate(oldUsers):
				if oldUser in newUsers:
					indexesToDelete.append(index)

			indexesToDelete.reverse()
			for index in indexesToDelete:
				del oldUsers[index]
			
			for oldUser in oldUsers:
				UserMeeting.objects.get(user=oldUser, meeting=meeting).delete()
			#######################################################################
			
			for user in newUsers:
				try:
					userMeeting = UserMeeting.objects.get(user=user, meeting=meeting) # existing users in the meeting
				except UserMeeting.DoesNotExist: # create the usermeeting	
					userMeeting = UserMeeting(user=user,
											meeting=meeting,
											is_Admin=False)
					userMeeting.save()					
				else:
					pass # user already exists, carry on
					
			return HttpResponseRedirect("/meeting/%s" % meetingId)		

	c = {}
	c.update(csrf(request))
	c.update({'meetingForm': meetingForm,  'meetingId': meetingId, 'sectionTitle': 'Edit Meeting',  'sections': sections})
	return render_to_response('editMeeting.html', c, context_instance=RequestContext(request))


def finalizeMeeting(request, meetingId):
	try:
		meeting = Meeting.objects.get(id=meetingId)
		
	except Meeting.DoesNotExist:
		raise Http404

	try:
		userMeeting = UserMeeting.objects.get(user=request.user, meeting=meeting)

	except UserMeeting.DoesNotExist:
		return HttpResponseForbidden("<h1>Forbidden</h1><p>user not authenticated</p>")
	
	if not userMeeting.is_Admin:
		return HttpResponseForbidden("<h1>Forbidden</h1><p>user is not admin to meeting</p>")
			
	ActionFormSet = formset_factory(ActionForm, extra=0)
	
	if request.method != 'POST':
		finalizeForm = FinalizeForm(initial={'discussions': meeting.discussions, 'conclusions': meeting.conclusions})

		initialFormData = []
		for tmpUserMeeting in UserMeeting.objects.filter(meeting=meeting):
			initialFormData.append({'actions': tmpUserMeeting.actions,
									'completedActions': tmpUserMeeting.completedActions,
									'userId': str(tmpUserMeeting.user.id),
									'name': '%s %s' % (tmpUserMeeting.user.first_name, tmpUserMeeting.user.last_name)})

		actionFormSet = ActionFormSet(initial=initialFormData)
		
	else:
		finalizeForm = FinalizeForm(request.POST)
		actionFormSet = ActionFormSet(request.POST)
		
		if finalizeForm.is_valid() and actionFormSet.is_valid():
			meeting.discussions=finalizeForm.cleaned_data['discussions']
			meeting.conclusions=finalizeForm.cleaned_data['conclusions']
			meeting.save()
			
			for actionForm in actionFormSet:
				userMeeting = UserMeeting.objects.get(user__id=int(actionForm.cleaned_data['userId']), meeting=meeting)
				userMeeting.actions = actionForm.cleaned_data['actions']
				userMeeting.completedActions = actionForm.cleaned_data['completedActions']
				userMeeting.save()
				
			return HttpResponseRedirect('/meeting/%s' % meetingId)

	c = {}
	c.update(csrf(request))
	c.update({'finalizeForm': finalizeForm, 'actionFormSet': actionFormSet, 'meetingId': meetingId,
			'sectionTitle': 'Finalize Meeting', 'sections': sections})
	return render_to_response('finalizeMeeting.html', c, context_instance=RequestContext(request))


def rsvpMeeting(request, meetingId):
	if not request.user.is_authenticated():
		return HttpResponseForbidden("<h1>Forbidden</h1><p>user not authenticated</p>")
	
	try:
		meeting = Meeting.objects.get(id=meetingId)
		
	except Meeting.DoesNotExist:
		raise Http404
		
	else:
		try:
			userMeeting = UserMeeting.objects.get(user=request.user, meeting=meeting)

		except UserMeeting.DoesNotExist:
			return HttpResponseForbidden("<h1>Forbidden</h1><p>user not authenticated</p>")
			
	if request.method != 'POST':
		return HttpResponseForbidden("<h1>Forbidden</h1><p>POST requests only</p>")
	else:
		rsvpForm = RSVPForm(request.POST)
		if rsvpForm.is_valid():
			userMeeting.rsvp_status = rsvpForm.cleaned_data['rsvp_choice']
			userMeeting.save()
			return HttpResponseRedirect('/meeting/%s' % meetingId)
	
def createComment(request, meetingId):
	if not request.user.is_authenticated():
		return HttpResponseForbidden("<h1>Forbidden</h1><p>user not authenticated</p>")

	try:
		meeting = Meeting.objects.get(id=meetingId)

	except Meeting.DoesNotExist:
		raise Http404

	else:
		try:
			userMeeting = UserMeeting.objects.get(user=request.user, meeting=meeting)

		except UserMeeting.DoesNotExist:
			return HttpResponseForbidden("<h1>Forbidden</h1><p>user not authenticated</p>")

	if request.method != 'POST':
		commentForm = CommentForm()
	else:
		commentForm = CommentForm(request.POST)
		if commentForm.is_valid():
			comment = Comment(user=request.user, meeting=meeting,
							text=commentForm.cleaned_data['text'], created_date_time=datetime.now())
			comment.save()
			return HttpResponseRedirect('/meeting/%s' % meetingId)
	c = {}
	c.update(csrf(request))
	c.update({'commentForm': commentForm, 'meetingId': meetingId,
			'sections': sections})
	return render_to_response('createComment.html', c, context_instance=RequestContext(request))
