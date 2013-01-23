from __init__ import *
from django.core import serializers

def api(request, resource):
	if request.method == 'GET':
		id = request.GET.get('id', '')
		query = request.GET.get('query', '')
		if resource == 'meeting' : return meetingResource(request, id)
		if resource == 'user' : return userResource(request, query)


def meetingResource(request, userId):
	if request.user.id == int(userId):
		return HttpResponse(serializers.serialize("json", request.user.meeting_set.all()))
	else:
		return HttpResponse(json.dumps({'API_ERROR': 'FORBIDDEN'}))

def userResource(request, query):
	userObjects = User.objects.filter( Q(first_name__icontains=query) | Q(last_name__icontains=query)
										| Q(username__icontains=query) ).exclude(id=request.user.id)
	users = []
	if query:
		for userObject in userObjects:
			users.append( {'first_name': userObject.first_name, 'last_name': userObject.last_name, 'username': userObject.username} )
	print users
	print HttpResponse(json.dumps(users, cls=DjangoJSONEncoder))
	return 	HttpResponse(json.dumps(users, cls=DjangoJSONEncoder))
	