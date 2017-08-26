from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

import json
from .models import *
from django.db.models import Q
# Create your views here.


@login_required()
def create_dweet_view(request):
    user_id = request.user.id
    user_dweet_count = 0
    context = {
        "user_id": user_id,
        "username": request.user.username
    }
    dweet_list = []
    try:
        dweets = Dweet.objects.filter(user_id_id=user_id).order_by('-dweeted_at')
        user_dweet_count = dweets.count()
        for dweet in dweets:
            dweet_obj = {
                'id': dweet.id,
                'username': dweet.user_id.username,
                'content': dweet.content,
                'dweeted_at': dweet.dweeted_at
            }
            try:
                comments = Comment.objects.filter(dweet_id_id=dweet.id)
                dweet_obj['comment_count'] = comments.count()
            except Exception as exception:
                print("Exception occurred while getting comments for a dweet : %s" % exception)
                return render(request, "dweet/create_dweet.html", context)
            try:
                likes = LikeDweet.objects.filter(dweet_id_id=dweet.id)
                dweet_obj['like_count'] = likes.count()
            except Exception as exception:
                print("Exception occurred while getting likes of the tweet : %s" % exception)
                return render(request, "dweet/create_dweet.html", context)
            dweet_list.append(dweet_obj)
        context['dweet_list'] = dweet_list
        context['dweet_count'] = user_dweet_count
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


@csrf_exempt
def like_dweet(request):
    user_id = request.user.id
    try:
        if request.method == "POST":
            data = json.loads(request.POST.get('data'))
            dweet_id = int(data['dweet_id'])
            try:
                likes = LikeDweet.objects.filter(
                    Q(dweet_id_id=dweet_id) & Q(user_id_id=user_id))
                if likes.count() >= 1:
                    return HttpResponse(json.dumps({
                        'statusCode': 1,
                        'statusMessage': "You already liked this dweet."
                    }), content_type='application/json')
                elif likes.count() == 0:
                    like = LikeDweet()
                    like.dweet_id_id = dweet_id
                    like.user_id_id = user_id
                    like.save()
                    return HttpResponse(json.dumps({
                        'statusCode': 0,
                        'statusMessage': "Liked successfully."
                    }), content_type='application/json')
            except Exception as exception:
                print("Exception occurred while getting or saving like dweet data : %s" % exception)
                return HttpResponse(json.dumps({
                    'statusCode': 1,
                    'statusMessage': "Exception occurred while getting or saving dweet data : %s" % exception
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


@csrf_exempt
def add_comment(request):
    user_id = request.user.id
    try:
        if request.method == "POST":
            data = json.loads(request.POST.get('data'))
            try:
                comment = Comment()
                comment.user_id_id = user_id
                comment.dweet_id_id = int(data['dweetId'])
                comment.content = str(data['content'])
                comment.save()
                return HttpResponse(json.dumps({
                    'statusCode': 0,
                    'statusMessage': "Comment added successfully."
                }), content_type='application/json')
            except Exception as exception:
                print("Exception occurred while saving comment to the database : %s" % exception)
                return HttpResponse(json.dumps({
                    'statusCode': 1,
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
    comments = []
    try:
        if request.method == "GET":
            comment_list = Comment.objects.filter(dweet_id_id=dweet_id)
            for comment in comment_list:
                comment_object = {
                    'id': comment.id,
                    'username': comment.user_id.username,
                    'content': comment.content,
                    'commented_at': str(comment.commented_at)
                }
                comments.append(comment_object)
            return HttpResponse(json.dumps({
                'statusCode': 0,
                'statusMessage': "Comments fetched successfully.",
                'comments': json.dumps(comments)
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