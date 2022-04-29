# import pymysql
# pymysql.install_as_MySQLdb()
# # 数据库
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'NLP_DataBase',
#         'USER': 'root',
#         'PASSWORD': '123456',
#         'HOST': '127.0.0.1'
#     }
# }
import pymysql
pymysql.version_info = (1, 4, 13, "final", 0)
pymysql.install_as_MySQLdb()