from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from .utils import OAuthQQ
from .exceptions import OAuthQQAPIError
from .models import OAuthQQUser
from .serializers import OAuthQQUserSerializer
from carts.utils import merge_cart_cookie_to_redis


# url(r'^qq/authorization/$', views.QQAuthURLView.as_view())

class QQAuthURLView(APIView):
    """
    获取QQ登录的url

    GET http://127.0.0.1:8000/oauth/qq/authorization/?next=xxx
    请求参数：查询字符串
    next：用户QQ登录成功后进入美多商城的哪个网址

    返回数据： JSON
    login_url：qq登录网址
    """
    def get(self, request):
        # 获取next参数
        next = request.query_params.get("next")

        # 拼接QQ登录的网址
        oauth_qq = OAuthQQ(state=next)
        login_url = oauth_qq.get_login_url()

        # 返回
        return Response({'login_url': login_url})

# url(r'^qq/user/$', views.QQAuthUserView.as_view())
class QQAuthUserView(CreateAPIView):
    """
    QQ登录的用户  ?code=xxxx

    GET /oauth/qq/user/?code=xxx
    请求参数： JSON 或 表单
    mobile：手机号
    password：密码
    sms_code：短信验证码
    access_token：凭据 （包含openid)

    返回数据： JSON
    token：JWT token
    user_id：用户id
    username：用户名

    POST /oauth/qq/user/
    请求参数： JSON 或 表单
    mobile：手机号
    password：密码
    sms_code：短信验证码
    access_token：据 （包含openid)

    返回数据： JSON
    token：JWT token
    user_id：用户id
    username：用户名
    """
    serializer_class = OAuthQQUserSerializer

    def get(self, request):
        # 获取code
        code = request.query_params.get('code')

        if not code:
            return Response({'message': '缺少code'}, status=status.HTTP_400_BAD_REQUEST)

        oauth_qq = OAuthQQ()
        try:
            # 凭借code 获取access_token
            access_token = oauth_qq.get_access_token(code)

            # 凭借access_token获取 openid
            openid = oauth_qq.get_openid(access_token)
        except OAuthQQAPIError:
            return Response({'message': '访问QQ接口异常'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # 根据openid查询数据库OAuthQQUser  判断数据是否存在
        try:
            oauth_qq_user = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 如果数据不存在，处理openid 并返回
            access_token = oauth_qq.generate_bind_user_access_token(openid)
            return Response({'access_token': access_token})

        else:
            # 如果数据存在，表示用户已经绑定过身份， 签发JWT token
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            user = oauth_qq_user.user
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            # return Response({
            #     'username': user.username,
            #     'user_id': user.id,
            #     'token': token
            # })
            response = Response({
                'username': user.username,
                'user_id': user.id,
                'token': token
            })

            # 合并购物车
            response = merge_cart_cookie_to_redis(request, user, response)

            return response

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # 合并购物车
        user = self.user
        response = merge_cart_cookie_to_redis(request, user, response)

        return response



















