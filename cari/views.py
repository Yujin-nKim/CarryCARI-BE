from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from .serializers import UserSerializer, ResultSerializer
from .models import User, Result

class UserInfo(APIView):
    def post(self, request):
        user_img_url = request.data.get("user_url")
        if user_img_url:
            user = User(user_img_url=user_img_url)
            user.save()
            serializer = UserSerializer(user)
            return Response(serializer.data, status=200)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ResultDetail(APIView):
    # result_id에 맞는 결과물 가져옴
    def get_result_url(self, result_id):
        try:
            result = Result.objects.get(result_id=result_id)
            return result.result_img_url
        except Result.DoesNotExist:
            raise Http404

    # user_id에 맞는 사용자 정보 가져옴
    def get_user_url(self, user_id):
        try:
            user = User.objects.get(user_id=user_id)
            return user.user_img_url
        except User.DoesNotExist:
            raise Http404

    def get(self, request):

        user_id = request.query_params.get('id')
        emotion = request.query_params.get('emotion')

        before_img = self.get_user_url(user_id)
        # TODO : before_img와 emotion을 ai모델에 input으로 넣어서 결과물 산출하기

        # TODO : 나온 결과물 DB(Result)에 저장하기

        after_img = self.get_result_url(user_id)  # 모델 돌린 결과 url

        return Response({
            "before_img": before_img,
            "after_img": after_img
        })
