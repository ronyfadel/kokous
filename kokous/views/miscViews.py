from __init__ import *

def misc(request):
	return render_to_response("misc.html", context_instance=RequestContext(request))