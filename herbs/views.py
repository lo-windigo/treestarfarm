from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import Context, loader
from herbs.models import Herb

def herb(request, findSlug):

	template = loader.get_template("pages/herb.html")

	# Get the herb from the slug sent in
	thisHerb = get_object_or_404(Herb, slug=findSlug)
	
	context = Context({"thisHerb": thisHerb})

	return HttpResponse(template.render(context))
