from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

import json
from .models import *
# Create your views here.


@login_required()
def create_dweet_view(request):
    user_id = request.user.id
    context = {
        "user_id": user_id,
        "username": request.user.username
    }
    dweet_list = []
    try:
        dweets = Dweet.objects.filter(user_id_id=user_id).order_by('-dweeted_at')
        count = dweets.count()
        context['dweet_count'] = count
        for dweet in dweets:
            dweet_obj = {
                'username': dweet.user_id.username,
                'content': dweet.content,
                'dweeted_at': dweet.dweeted_at
            }
            dweet_list.append(dweet_obj)
        context['dweet_list'] = dweet_list
        return render(request, "dweet/create_dweet.html", context)
    except Exception as exception:
        print("Exception occurred while getting dweet feed : %s" %exception)
        return render(request, "dweet/create_dweet.html", context)



@csrf_exempt
def add_dweet(request):
    try:
        if request.method == "POST":
            data = json.loads(request.POST.get('data'))
            print data
            content = data['content']
            try:
                dweet = Dweet()
                dweet.user_id_id = int(request.user.id)
                dweet.content = content
                dweet.save()
            except Exception as exception:
                print("Exception occurred while saving dweet : %s" % exception)
                return HttpResponse(json.dumps({
                    'statusCode': 1,
                    'statusMessage': "Exception occurred while saving dweet : %s" % exception
                }))
            return HttpResponse(json.dumps({
                'statusCode': 0,
                'statusMessage': "Dweet added successfully."
            }), content_type='application/json')
        else:
            return HttpResponse(json.dumps({
                'statusCode': 1,
                'statusMessage': "Not a POST request."
            }), content_type='application/json')
    except Exception as exception:
        print("Exception occurred while adding a dweet : %s" % exception)
        return HttpResponse(json.dumps({
            'statusCode': 1,
            'statusMessage': "Exception occurred while adding a dweet : %s" % exception
        }), content_type='application/json')


@login_required()
def get_dweets(request, user_id):
    dweets = []
    try:
        if request.method == "GET":
            followUserList = FollowUser.objects.filter(followed_by_id=user_id)
            return HttpResponse(json.dumps({
                'statusCode': 0,
                'statusMessage': "Dweets fetched successfully."
            }), content_type='application/json')
        else:
            return HttpResponse(json.dumps({
                'statusCode': 1,
                'statusMessage': "Not a get request."
            }), content_type='application_json')
    except Exception as exception:
        print("Exception occurred while getting dweets : %s" % exception)
        return HttpResponse(json.dumps({
            'statusCode': 1,
            'statusMessage': "Exception occurred while getting dweets : %s" % exception
        }), content_type='application/json')


def delete_dweet(request, dweet_id):
    try:
        if request.method == "DELETE":
            return HttpResponse(json.dumps({
                'statusCode': 0,
                'statusMessage': 'Dweet deleted successfully.'
            }), content_type='application/json')
        else:
            return HttpResponse(json.dumps({
                'statusCode': 1,
                'statusMessage': "Not a DELETE request."
            }), content_type='application/json')
    except Exception as exception:
        print("Exception occurred while deleting a dweet : %s" %exception)
        return HttpResponse(json.dumps({
            'statusCode': 1,
            'statusMessage': "Exception occurred while deleting a dweet : %s" %exception
        }), content_type='application/json')


def like_dweet(request):
    try:
        if request.method == "POST":
            return HttpResponse(json.dumps({
                'statusCode': 0,
                'statusMessage': "Liked successfully."
            }), content_type='application/json')
        else:
            return HttpResponse(json.dumps({
                'statusCode': 1,
                'statusMessage': "Not a POST request."
            }), content_type='application/json')
    except Exception as exception:
        print("Exception occurred while liking a dweet : %s" % exception)
        return HttpResponse(json.dumps({
            'statusCode': 1,
            'statusMessage': "Exception occurred while liking a dweet : %s" %exception
        }), content_type='application/json')


def add_comment(request):
    try:
        if request.method == "POST":
            return HttpResponse(json.dumps({
                'statusCode': 0,
                'statusMessage': "Comment added successfully."
            }), content_type='application/json')
        else:
            return HttpResponse(json.dumps({
                'statusCode': 1,
                'statusMessage': "Not a POST request."
            }), content_type='application/json')
    except Exception as exception:
        print("Exception occurred while adding a comment to dweet : %s" % exception)
        return HttpResponse(json.dumps({
            'statusCode': 1,
            'statusMessage': "Exception occurred while adding a comment to the dweet : %s" % exception
        }), content_type='application/json')


def get_comments(request, dweet_id):
    try:
        if request.method == "GET":
            return HttpResponse(json.dumps({
                'statusCode': 0,
                'statusMessage': "Comments fetched successfully."
            }), content_type='application/json')
        else:
            return HttpResponse(json.dumps({
                'statusCode': 1,
                'statusMessage': "Not a GET request."
            }), content_type='application/json')
    except Exception as exception:
        print("Exception occurred while getting comments for a dweet : %s" % exception)
        return HttpResponse(json.dumps({
            'statusCode': 1,
            'statusMessage': "Exception occurred while getting comments for a dweet : %s" % exception
        }), content_type='application/json')


def follow_user(request):
    try:
        if request.method == "POST":
            return HttpResponse(json.dumps({
                'statusCode': 0,
                'statusMessage': "Operation successful."
            }), content_type='application/json')
        else:
            return HttpResponse(json.dumps({
                'statusCode': 1,
                'statusMessage': "Not a POST request."
            }), content_type='application/json')
    except Exception as exception:
        print("Exception occurred while following a user : %s" % exception)
        return HttpResponse(json.dumps({
            'statusCode': 1,
            'statusMessage': "Exception occurred while following a user : %s" % exception
        }), content_type='application/json')