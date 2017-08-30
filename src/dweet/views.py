from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

import json
from .models import *
from django.db.models import Q
from django.contrib.auth.models import User
# Create your views here.


@login_required()
def create_dweet_view(request):
    user_id = request.user.id
    user_dweet_count = 0
    user_following_count = 0
    user_follower_count = 0
    context = {
        "user_id": user_id,
        "username": request.user.username
    }
    dweet_list = []
    try:
        following = FollowUser.objects.filter(followed_by_id=user_id)
        user_following_count = following.count()
        dweets = Dweet.objects.filter(Q(user_id_id=user_id) |
                                      Q(user_id_id__in=[follow_object.followed_to_id for follow_object in following])).order_by('-dweeted_at')
        for dweet in dweets:
            if dweet.user_id_id == user_id:
                user_dweet_count += 1
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
        followers = FollowUser.objects.filter(followed_to_id=user_id)
        user_follower_count = followers.count()
        context['following_count'] = user_following_count
        context['follower_count'] = user_follower_count
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


@csrf_exempt
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


@csrf_exempt
def follow_user(request):
    user_id = request.user.id
    try:
        if request.method == "POST":
            data = json.loads(request.POST.get('data'))
            follow_to = int(data['followed_to_id'])
            follow_by = user_id
            try:
                follow_object = FollowUser()
                follow_object.followed_by_id = follow_by
                follow_object.followed_to_id = follow_to
                follow_object.save()
                return HttpResponse(json.dumps({
                    'statusCode': 0,
                    'statusMessage': "Followed successfully."
                }), content_type='application/json')
            except Exception as exception:
                print("Exception occurred while following a user : %s" % exception)
                return HttpResponse(json.dumps({
                    'statusCode': 1,
                    'statusMessage': "Exception occurred while following a user : %s" % exception
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


@csrf_exempt
def show_following(request):
    context = {}
    user_id = request.user.id
    following_user_list = []
    try:
        if request.method == "GET":
            following_users = FollowUser.objects.filter(followed_by_id=user_id)
            for following_user in following_users:
                following_user_object = {
                    'followed_to_id': following_user.followed_to_id,
                    'followed_to_name': following_user.followed_to.username
                }
                following_user_list.append(following_user_object)
            context['following_user_list'] = following_user_list
            return render(request, "dweet/following_user_list.html", context)
        else:
            return render(request, "dweet/following_user_list.html", context)
    except Exception as exception:
        print("Exception occurred while getting list of users whom you follow : %s" % exception)
        return render(request, "dweet/following_user_list.html", context)


@csrf_exempt
def show_follower(request):
    context = {}
    user_id = request.user.id
    follower_user_list = []
    try:
        if request.method == "GET":
            follower_users = FollowUser.objects.filter(followed_to_id=user_id)
            for follower_user in follower_users:
                follower_user_object = {
                    'followed_by_id': follower_user.followed_by_id,
                    'followed_by_name': follower_user.followed_by.username
                }
                follower_user_list.append(follower_user_object)
            context['follower_user_list'] = follower_user_list
            return render(request, "dweet/follower_user_list.html", context)
        else:
            return render(request, "dweet/follower_user_list.html", context)
    except Exception as exception:
        print("Exception occurred while getting list of followers : %s" % exception)
        return render(request, "dweet/follower_user_list.html", context)


@csrf_exempt
def unfollow_user(request):
    user_id = request.user.id
    try:
        if request.method == "POST":
            data = json.loads(request.POST.get('data'))
            followed_to_id = int(data['followed_to_id'])
            try:
                follow_user = FollowUser.objects.get(Q(followed_by_id=user_id) & Q(followed_to_id=followed_to_id))
                follow_user.delete()
                return HttpResponse(json.dumps({
                    'statusCode': 0,
                    'statusMessage': "You un-followed a user successfully."
                }), content_type='application/json')
            except Exception as exception:
                print("Exception occurred while removing follow-ship : %s" % exception)
                return HttpResponse(json.dumps({
                    'statusCode' : 1,
                    'statusMessage': "Exception occurred while removing follow-ship : %s" % exception
                }), content_type='application/json')
        else:
            return HttpResponse(json.dumps({
                'statusCode': 1,
                'statusMessage': "Not a POST method."
            }), content_type='application/json')
    except Exception as exception:
        print("Exception occurred while un-following a particular user : %s" % exception)
        return HttpResponse(json.dumps({
            'statusCode': 1,
            'statusMessage': "Exception occurred while un-following a particular user : %s" % exception
        }), content_type='application/json')


@csrf_exempt
def show_search_results(request, search):
    user_id = 4
    print(search)
    context = {}
    dweet_list = []
    follow_user_list = []
    not_follow_user_list = []
    user_list = {}
    try:
        user = User.objects.get(id=user_id)
        follow_users = FollowUser.objects.filter(followed_by_id=user_id).filter(followed_to__username__icontains=search)

        for user_obj in follow_users:
            follow_user_obj = {
                'id': user_obj.followed_to_id,
                'username': user_obj.followed_to.username
            }
            follow_user_list.append(follow_user_obj)
        print follow_user_list
        not_follow_users = User.objects.filter(username__icontains=search).exclude(id=user_id)\
            .exclude(id__in=[follow_object.followed_to_id for follow_object in follow_users])
        for user_obj in not_follow_users:
            not_follow_user_obj = {
                'id': user_obj.id,
                'username': user_obj.username
            }
            not_follow_user_list.append(not_follow_user_obj)
        user_list['follow_users'] = follow_user_list
        user_list['not_follow_users'] = not_follow_user_list

        following = FollowUser.objects.filter(followed_by_id=user_id)
        print(following)
        dweets = Dweet.objects.filter(Q(user_id_id=user_id) |
                                      Q(user_id_id__in=[follow_object.followed_to_id for follow_object in
                                                        following])).filter(content__icontains=search).order_by('-dweeted_at')
        for dweet in dweets:
            dweet_object = {
                'id': dweet.id,
                'username': dweet.user_id.username,
                'content': dweet.content,
                'dweeted_at': dweet.dweeted_at
            }
            dweet_list.append(dweet_object)
        context['users'] = user_list
        context['dweets'] = dweet_list
        print(context)
        return render(request, "dweet/search_result.html", context)
    except Exception as exception:
        print("Exception occurred while getting search results : %s" % exception)
        return render(request, "dweet/search_result.html", context)
    pass