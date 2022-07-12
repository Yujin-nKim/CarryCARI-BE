from django.db import models


# 사용자 이미지 저장
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_img_url = models.ImageField(upload_to='user_images/%Y/%m/%d/', blank=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.user_id}]'


# 결과물 이미지 저장
class Result(models.Model):
    result_id = models.AutoField(primary_key=True)
    result_img_url = models.ImageField(upload_to='result_images/%Y/%m/%d/', blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    result_emotion = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'[{self.result_id}]'
