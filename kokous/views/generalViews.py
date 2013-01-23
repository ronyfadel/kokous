from __init__ import *

def home(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/profile/')
	else:
		c = {}
		c.update(csrf(request))
		c.update({'loginForm': LoginForm(), 'signupForm': SignupForm()})
		return render_to_response('index.html', c, context_instance=RequestContext(request))

def signup(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/profile/') # if user is already signed up, redirect to profile
	c = {}
	c.update(csrf(request))

	if request.method != 'POST':
		signupForm = SignupForm()

	else:
		signupForm = SignupForm(request.POST)
		if signupForm.is_valid():
			cleaned_data = signupForm.cleaned_data
				
			# Creating user
			new_user = User.objects.create_user(username=cleaned_data['username'], email=cleaned_data['email_address'])

			new_user.first_name=cleaned_data['first_name'].capitalize() # Django doesn't do that for you!
			new_user.last_name=cleaned_data['last_name'].capitalize()
			new_user.set_password(cleaned_data['password'])
			new_user.save()
			
			# Creating user profile
			userProfile = UserProfile(user=new_user)
			userProfile.save()
			
			# Logging him in
			user = auth.authenticate(username=cleaned_data['username'], password=cleaned_data['password'])
			auth.login(request, user)
				
			return HttpResponseRedirect('/profile/')
				
	c.update({'signupForm' : signupForm})
	return render_to_response('signup.html', c, context_instance=RequestContext(request))

def login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/profile/') # if user is already signed up, redirect to profile

	if request.method != 'POST':
		loginForm = LoginForm()

	else:
		loginForm = LoginForm(request.POST)
		if loginForm.is_valid():
			user = auth.authenticate(username=loginForm.cleaned_data['username'], password=loginForm.cleaned_data['password'])
			auth.login(request, user)
			return HttpResponseRedirect('/profile/')

	c = {}
	c.update(csrf(request))
	c.update({'loginForm' : loginForm})
	return render_to_response('login.html', c, context_instance=RequestContext(request))

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/")
