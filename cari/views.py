from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from ml import ai
from .models import User, Result
# serializers
from .serializers import UserSerializer, ResultSerializer
# email
from django.core.mail import BadHeaderError, send_mail
from .email import send_email, html_message, sender, subject
from pathlib import Path

class UserInfo(APIView):
    def post(self, request):
        user_img = request.FILES.get("image")
        if user_img:
            user = User(user_img=user_img)
            user.save()
            serializer = UserSerializer(user)
            return Response(serializer.data, status=200)
        return Response(status=status.HTTP_400_BAD_REQUEST)

        # user_img_url = request.data.get("user_url")
        # if user_img_url:
        #     user = User(user_img_url=user_img_url)
        #     user.save()
        #     serializer = UserSerializer(user)
        #     return Response(serializer.data, status=200)
        # return Response(status=status.HTTP_400_BAD_REQUEST)

class SendEmail(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        user_email = request.data.get('user_email')

        # Todo : 결과 이미지와 link 시키기
        image_path = "result_path"
        image_name = Path(image_path).name
        text_message = f"Email with a nice embedded image {image_name}."

        if image_path:
            send_email(subject=subject, text_content=text_message, html_content=html_message, sender=sender,
                       recipient=user_email, image_path=image_path, image_name=image_name)
            return Response(status=200)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class ResultDetail(APIView):
    # result_id에 맞는 결과물 가져옴
    def get_result_img(self, user_id):
        try:
            result = Result.objects.get(user_id=user_id)
            return result.result_img
        except Result.DoesNotExist:
            raise Http404

    # user_id에 맞는 사용자 정보 가져옴
    def get_user_img(self, user_id):
        try:
            user = User.objects.get(user_id=user_id)
            return user.user_img
        except User.DoesNotExist:
            raise Http404

    def get(self, request):

        user_id = request.query_params.get('id')
        emotion = request.query_params.get('emotion')

        before_img = self.get_user_img(user_id).url
        # TODO : before_img와 emotion을 ai모델에 input으로 넣어서 결과물 산출하기

        user_id = 4

        image_path = ""
        emotion = 3

        ai.generate_imageclip(user_id, image_path, emotion)
        # TODO : 나온 결과물 DB(Result)에 저장하기

        after_img = self.get_result_img(user_id).url  # 모델 돌린 결과 url

        return Response({
            "before_img": before_img,
            "after_img": after_img
        })
