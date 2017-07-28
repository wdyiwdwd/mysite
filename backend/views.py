from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Test
from .forms import TestForm
from dwebsocket.decorators import accept_websocket,require_websocket
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
import json
# Create your views here.


def signup_submit(request):
	username = request.GET.get('username')
	password = request.GET.get('password')
	print(username)
	print(password)
	try:
		user = User.objects.create_user(username=username, password=password)
		return HttpResponse("signup success")
	except:
		return HttpResponse("signup failure")

@csrf_exempt
def login_submit(request):
	print(request.body.decode('utf-8'))
	body_unicode = request.body.decode('utf-8')
	body = json.loads(body_unicode)
	user = auth.authenticate(request, username=body['username'], password=body['password'])
	if not user:
		return HttpResponse("login failure")
	auth.login(request, user)
	return HttpResponse("login success")

def query_repeat_username(request):
	get_username = request.GET.get('reusername')
	print(get_username)
	try:
		has_email = User.objects.get(username=get_username)
		if(has_email):
			return HttpResponse("username repeat")			
	except:
		return HttpResponse("username is ok") 

def insert(request):
	params = request.POST if request.method == 'POST' else None
	form = PostForm(params)
	if form.is_valid():
		form.save()
		return HttpResponse("insert success")
	return HttpResponse("insert failure")


@require_websocket
def websocket(request):
	for message in request.websocket:
		params = {'content' :message.decode(encoding='utf-8')}
		form = TestForm(params)
		if form.is_valid():
			form.save()
			request.websocket.send("insert success: ".encode(encoding='utf-8') + message)
		else:
			request.websocket.send("insert failure: ".encode(encoding='utf-8') + message)