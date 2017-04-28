from django.shortcuts import render

# Create your views here.

def index(request):
	return render(request, 'index.html', {})

def newpage(request):
	error = None
	if(3 > 2):
		error = "error"
	return render(request, 'newpage.html', {'error':error})