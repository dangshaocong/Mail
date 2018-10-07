import requests

########################### 用户部分 #########################################
""" 图片验证码 """
# url = "http://127.0.0.1:8000/image_codes/123456"
# requests.get(url)

""" 短信验证码 """
# url = "http://127.0.0.1:8000/sms_codes/13388888888/?image_code_id=123456&text=AAAA"
# response = requests.get(url)
# print(response.text)

""" 注册 """
# url = 'http://127.0.0.1:8000/users/'
# data = {'username': 'admin',
#         'password': 'admin123',
#         "password2":"admin123",
#         "sms_code":666666,
#         "mobile":13388888888,
#         "allow": "true"
#         }
# response = requests.post(url, data)
# print(response.text)

""" 登陆 """
url = 'http://127.0.0.1:8000/authorizations/'
data = {'username': 'admin', 'password': 'admin123'}
response = requests.post(url, data)
response = response.text
token = response.split(":")[1].split(",")[0]
print(token)

""" 用户名数量 """
# url = "http://127.0.0.1:8000/usernames/admin/count/"
# response = requests.get(url)
# print(response.text)

""" 手机号数量 """
# url = "http://127.0.0.1:8000/mobiles/13388888888/count/"
# response = requests.get(url)
# print(response.text)


""" 用户个人中心 """
# url2 = "http://127.0.0.1:8000/user/"
# headers = {
#     'Authorization': "JWT " + token
#     # 'Authorization': "JWT " + "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTM3Njg5NzM0LCJlbWFpbCI6IiJ9.OCmiX_MU9CVj55Zx4qBynA7Dq3EsR_HFOYfMbwKuf_U"
#
# }
# response2 = requests.get(url2, headers=headers)
# print(response2.text)

""" 请求省份数据 """
# url = "http://127.0.0.1:8000/areas/"
""" 请求城市或区县数据 """
# url = "http://127.0.0.1:8000/areas/420000/"
# response = requests.get(url)
# print(response.text)


################################### 商品部分 ############################

url2 = "http://127.0.0.1:8000/browse_histories/1"
headers = {
    'Authorization': 'JWT ' + "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTM3NjkwMDYyLCJlbWFpbCI6IiJ9.6I46j3nbledfhhgND9X67wpqae-SdTFn_6td-QqN4BI"

}
response2 = requests.post(url2, headers=headers)
print(response2.text)


requests.request()