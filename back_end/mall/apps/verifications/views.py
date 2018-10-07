import random

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from mall.libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from rest_framework.generics import GenericAPIView
from rest_framework import status
from logging import getLogger


from . import constants
from .serializers import ImageCodeCheckSerializer
from mall.utils.yuntongxun.sms import CCP
from tasks.sms.tasks import send_sms_code

logger = getLogger('django')


# url(r'^image_codes/(?P<image_code_id>[\w-]+)/$', views.ImageCodeView.as_view()),
# GET 127.0.0.1:8000/image_codes/123456
class ImageCodeView(APIView):
    """
    图片验证码
    请求参数：
    image_code_id：图片验证码编号
    """

    def get(self, request, image_code_id):
        """
        生成验证码图片
        :param request:
        :param image_code_id:
        :return: 返回图片
        """

        text, image = captcha.generate_captcha()
        text = "AAAA"

        # 保存真实值
        redis_conn = get_redis_connection('verify_codes')
        redis_conn.setex("img_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)

        logger.info("图片验证码：%s" % text)

        return HttpResponse(image, content_type='image/jpg')


# url('^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeView.as_view()),
# GET 127.0.0.1:8000/sms_codes/13388888888/?image_code_id=123456&text=AAAA
class SMSCodeView(GenericAPIView):
    """
    短信验证码
    请求参数：
    mobile:手机号
    image_code_id:图片验证码编号
    text:用户输入的图片验证码
    """
    serializer_class = ImageCodeCheckSerializer

    def get(self, request, mobile):
        # 校验参数由序列化器完成
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        # 生成短信验证码
        sms_code = '%06d' % random.randint(0, 999999)
        sms_code = "666666"


        logger.info("短信验证码：%s" % sms_code)

        # 保存短信验证码  保存发送记录
        redis_conn = get_redis_connection('verify_codes')
        # redis_conn.setex("sms_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # redis_conn.setex("send_flag_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)

        # redis管道
        pl = redis_conn.pipeline()
        pl.setex("sms_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex("send_flag_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)

        # 让管道通知redis执行命令
        pl.execute()

        # 使用celery发送短信验证码
        # expires = constants.SMS_CODE_REDIS_EXPIRES // 60
        # send_sms_code.delay(mobile, sms_code, expires, constants.SMS_CODE_TEMP_ID)

        return Response({'message': 'OK'})
