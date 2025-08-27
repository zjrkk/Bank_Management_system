from django.urls import path
from . import views
from . import captcha  # 假设您会创建一个captcha.py文件

urlpatterns = [
    path('', views.login_view, name='login'),
    path('index/', views.index_view, name='index'),
    path('credit/', views.credit_view, name='credit'),
    path('wealth/', views.wealth_view, name='wealth'),
    path('life/', views.life_view, name='life'),
    path('mine/', views.mine_view, name='mine'),
    path('verify_password/', views.verify_password, name='verify_password'),
    path('superadmin/', views.superadmin_view, name='superadmin'),
    path('superadmin/add/', views.add_user, name='add_user'),
    path('superadmin/edit/<int:id>/', views.edit_user, name='edit_user'),
    path('superadmin/delete/<int:id>/', views.delete_user, name='delete_user'),
    # 新增验证码路由
    path('captcha/', captcha.generate_captcha, name='captcha'),

    # ...其他路由...
path('mymoney/', views.mymoney_view, name='mymoney'),
    path('api/get_balance/', views.get_balance_api, name='get_balance_api'),
    path('mymoney/', views.mymoney_view, name='mymoney'),
#     path('api/get_balance/', views.get_balance_api, name='get_balance_api'),
#
# # ...其他路由...
#     path('add-transaction/', views.add_transaction, name='add_transaction'),
#

]