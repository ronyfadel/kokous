
# Django specifics
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseForbidden
from django.template import RequestContext
from django.core.context_processors import csrf

# Forms
from kokous.forms import SignupForm, LoginForm, MeetingForm, SettingsForm, FinalizeForm, ActionForm, RSVPForm, CommentForm
from django.forms.util import ErrorList	# to inject errors in forms
from django.forms.formsets import formset_factory # to create formsets

# Models and auth
from django.contrib.auth.models import User
from django.contrib import auth
from kokous.models import UserProfile, Meeting, UserMeeting, Comment
from django.db.models import Q # The Magic Stick, to be able to customize queries

# Utilities
import inspect # to get method name from method (inspect stack)
from datetime import datetime, date, timedelta

# For JSON parsing
import json
from django.core.serializers.json import DjangoJSONEncoder

# Sections for each User
sections = ["profile", "meetings", "settings"]