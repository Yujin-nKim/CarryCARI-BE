from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from .models import User, Result

# serializers
from .serializers import UserSerializer, ResultSerializer

# email
from django.core.mail import BadHeaderError, send_mail
from .email import send_email, html_message, sender, subject
from pathlib import Path
import shutil, os

# run AImodel
from . import StyleCariGAN
from . import StyleCLIP

class UserInfo(APIView):
    def post(self, request):
        user_img = request.FILES.get("image")
        if user_img:
            user = User(user_img=user_img)
            user.save()
            serializer = UserSerializer(user)

            # save user image in another directory
            src = '/home/teamg/volume/CarryCARI-BE/_media/{filename}'.format(filename=user.user_img.name)
            # src = './_media/{filename}'.format(filename=user.user_img.name)

            # make directory
            dest = "/home/teamg/volume/CarryCARI-BE/assets/user_img/{user_id}".format(user_id=user.user_id)
            # dest = "./assets/user_img/{user_id}".format(user_id=user.user_id)
            os.makedirs(dest)

            # copy to new directory
            shutil.copy(src, dest)

            return Response(serializer.data, status=200)

        return Response(status=status.HTTP_400_BAD_REQUEST)


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
    def get_result(self, user_id):
        try:
            result = Result.objects.filter(user_id=user_id)
            return result
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
        emotion = int(request.query_params.get('emotion'))
        user = User.objects.get(user_id=user_id)

        before_img = self.get_user_img(user_id).url

        if emotion == 0: #stylecarigan만 실행
            print("======func1======")
            print("StyleCariGAN만 실행...")
            StyleCariGAN.run_StyleCariGAN(user, user_id, emotion)
        else: #styleclip -> stylecarigan 실행
            print("======func2, emotion = " + str(emotion) +"======")
            print("StyleCLIP 실행...")
            StyleCLIP.run_StyleCLIP(user, user_id, emotion)
            print("StyleCariGAN 실행...")
            StyleCariGAN.run_StyleCariGAN(user, user_id, emotion)

        result_image_path = '/home/teamg/volume/CarryCARI-BE/ml/StyleCariGAN/final_result/' 
        file_list = os.listdir(result_image_path)

        for item in file_list:
            result = Result()
            result.user_id = User.objects.get(user_id=user_id)
            image_path = f'/home/teamg/volume/CarryCARI-BE/ml/StyleCariGAN/final_result/{item}' 
            upload_path = f'/home/teamg/volume/CarryCARI-BE/_media/result_images/{item}'

            shutil.copy(image_path, upload_path)
            result.result_img_path = f'/_media/result_images/{item}'

            result.result_emotion = emotion
            result.save()

        result = self.get_result(user_id) 

        # after_img = self.get_result_img(user_id).url  # 모델 돌린 결과 url

        return Response({
            "before_img": before_img,
            "after_img_1": result[0].result_img_path,
            "after_img_2": result[1].result_img_path,
            "after_img_3": result[2].result_img_path,
            "after_img_4": result[3].result_img_path,
            "after_img_5": result[4].result_img_path,
            "after_img_6": result[5].result_img_path,
            "after_img_7": result[6].result_img_path,
            "after_img_8": result[7].result_img_path
        })