import json
from http import HTTPStatus

# from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
# from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework.decorators import api_view
# from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response

from blog.models import Post
from blog.api.serializers import PostSerializer


# def post_to_dict(post):
#     return {
#         "pk": post.pk,
#         "author_id": post.author_id,
#         "created_at": post.created_at,
#         "modified_at": post.modified_at,
#         "published_at": post.published_at,
#         "title": post.title,
#         "slug": post.slug,
#         "summary": post.summary,
#         "content": post.content,
#     }


# @csrf_exempt
@api_view(["GET", "POST"])
def post_list(request , format=None):
    if request.method == "GET":
        # posts = Post.objects.all()
        # posts_as_dict = [post_to_dict(p) for p in posts]
        # return JsonResponse({"data": posts_as_dict})
        posts = Post.objects.all()
        return JsonResponse({"data": PostSerializer(posts, many=True).data})
    elif request.method == "POST":
        # post_data = json.loads(request.body)
        # post = Post.objects.create(**post_data)
        # return HttpResponse(
        #     status=HTTPStatus.CREATED,
        #     headers={"Location": reverse("api_post_detail", args=(post.pk,))},
        # )
        serializer = PostSerializer(data=post_data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(
                status=HTTPStatus.CREATED,
                headers={"Location": reverse("api_post_detail", args=(post.pk,))},
            )

        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def post_detail(request, pk, format=None):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=HTTPStatus.NOT_FOUND)


    if request.method == "GET":
        # return JsonResponse(post_to_dict(post))
        # return JsonResponse(PostSerializer(post).data)
        return Response(PostSerializer(post).data)
    elif request.method == "PUT":
        # post_data = json.loads(request.body)
        # for field, value in post_data.items():
        #     setattr(post, field, value)
        # post.save()
        serializer = PostSerializer(post, data=request.data)
        # serializer = PostSerializer(post, data=post_data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=HTTPStatus.NO_CONTENT)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)

    elif request.method == "DELETE":
        post.delete()
        return Response(status=HTTPStatus.NO_CONTENT)   

        
    