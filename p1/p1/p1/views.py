import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserMsg
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import UserMsg, Transaction
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import datetime
from django.utils import timezone
import random
from .models import UserMsg, Transaction
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserMsg, Transaction
from .forms import TransactionForm
from django.http import JsonResponse
# 数据库操作
from TestModel.models import Test

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# 登录视图
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_captcha = request.POST.get('captcha', '').upper()
        session_captcha = request.session.get('captcha', '')

        # 先验证验证码
        if not session_captcha or user_captcha != session_captcha:
            return render(request, 'login.html', {'error': '验证码错误'})

        # 验证码验证通过后删除session中的验证码
        del request.session['captcha']

        try:
            user = UserMsg.objects.get(username=username, password=password)
            request.session['username'] = username  # 存入 session
            return redirect('index')
        except UserMsg.DoesNotExist:
            return render(request, 'login.html', {'error': '用户名或密码错误'})

    return render(request, 'login.html')
# 首页视图——导航栏第一个板块
def index_view(request):
    username = request.session.get('username', '游客')  # 从 session 取用户名，没有就显示“游客”
    # 这里用你 index 视图里的新闻数据
    news_data = [
        {
            'id': 1,
            'title': '加快科技创新，亟待金融再发力（财经眼）——加快构建科技金融体制大家谈',
            'source': '环球网',
            'publish_date': '2025-05-07 18:34',
            'url': 'https://finance.sina.com.cn/jjxw/2025-06-16/doc-infafyah3215063.shtml'
        },
        {
            'id': 2,
            'title': '深度解读5月金融数据，谁是社融多增的最大“功臣”',
            'source': '北京商报官方账号',
            'publish_date': '2025-05-07 09:59',
            'url': 'https://news.qq.com/rain/a/20250614A022U600'
        },
        {
            'id': 3,
            'title': '以金融和公用事业为主要配置',
            'source': '南京晨报 ',
            'publish_date': '2025-05-07 16:07',
            'url': 'https://www.msn.cn/zh-cn/news/other/%E4%BB%A5%E9%87%91%E8%9E%8D%E5%92%8C%E5%85%AC%E7%94%A8%E4%BA%8B%E4%B8%9A%E4%B8%BA%E4%B8%BB%E8%A6%81%E9%85%8D%E7%BD%AE/ar-AA1GLpRw?ocid=feedsansarticle'
        },
        {
            'id': 4,
            'title': '王沪宁在两岸融合发展示范区建设专题推进会上强调 高质量建设两岸融合发展示范区',
            'source': '新华社',
            'publish_date': '2025-05-08 15:57',
            'url': 'https://www.financialnews.com.cn/2025-06/16/content_427314.html'
        },
        {
            'id': 5,
            'title': '2025年一季度银行业运行情况分析报告',
            'source': '中国人民银行',
            'publish_date': '2025-04-30 10:20',
            'url': 'https://example.com/news5'
        },
        {
            'id': 6,
            'title': '数字人民币应用场景再拓展，覆盖更多民生领域',
            'source': '经济日报',
            'publish_date': '2025-04-28 14:35',
            'url': 'https://example.com/news6'
        },
        {
            'id': 7,
            'title': '多元金融板块异动拉升，弘业期货涨停',
            'source': '每日经济新闻',
            'publish_date': '2025-04-25 09:10',
            'url': 'https://www.msn.cn/zh-cn/news/other/%E5%A4%9A%E5%85%83%E9%87%91%E8%9E%8D%E6%9D%BF%E5%9D%97%E5%BC%82%E5%8A%A8%E6%8B%89%E5%8D%87-%E5%BC%98%E4%B8%9A%E6%9C%9F%E8%B4%A7%E6%B6%A8%E5%81%9C/ar-AA1GLHJU?ocid=BingNewsLanding&cvid=9985df5ebca944a38b48847ec3e36154&ei=12'
        },
        {
            'id': 8,
            'title': '【开源非银高超团队】关注陆家嘴金融论坛表态，港交所受益于金融开放',
            'source': '市场资讯',
            'publish_date': '2025-04-20 16:42',
            'url': 'https://finance.sina.com.cn/roll/2025-06-15/doc-infaeftf8558079.shtml'
        },
        {
            'id': 9,
            'title': '中国排名前二十的金融学家：思想领航，智启未来 ',
            'source': '人民网',
            'publish_date': '2025-06-16 11:21',
            'url': 'https://www.sohu.com/a/904766945_121261015'
        },
        {
            'id': 10,
            'title': '推动科技和金融“双向奔赴”——四部门详解15项科技金融政策举措',
            'source': '新华社',
            'publish_date': '2025-05-23 07:23 ',
            'url': 'https://www.gov.cn/zhengce/202505/content_7024946.htm'
        }
    ]
    paginator = Paginator(news_data, 3)
    page = request.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    context = {
        'username': username,  # 把 username 传给模板
        'news': news,
    }
    return render(request, 'index.html', context)


# 信用卡页面视图——导航栏第二个板块
def credit_view(request):
    return render(request, 'credit.html')

#财富视图——导航栏第三个板块
def wealth_view(request):
    return render(request, 'wealth.html')

#生活视图——导航栏第四个板块
def life_view(request):
    return render(request, 'life.html')


#我的视图——导航栏第五个板块
def mine_view(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    try:
        user = UserMsg.objects.get(username=username)
    except UserMsg.DoesNotExist:
        return redirect('login')

    context = {
        'username': user.username,
        'password': user.password,
        'cardid': user.cardid,
        'money': user.money,
    }
    return render(request, 'mine.html', context)




#后台显示界面
def superadmin_view(request):
    users = UserMsg.objects.all()
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'superadmin.html', {'page_obj': page_obj})
def add_user(request):
    if request.method == "POST":
        UserMsg.objects.create(
            username=request.POST['username'],
            password=request.POST['password'],
            cardid=request.POST['cardid'],
            money=request.POST['money']
        )
        return redirect('superadmin')
    return render(request, 'add_user.html')
def edit_user(request, id):
    user = get_object_or_404(UserMsg, pk=id)
    if request.method == "POST":
        user.username = request.POST['username']
        user.password = request.POST['password']
        user.cardid = request.POST['cardid']
        user.money = request.POST['money']
        user.save()
        return redirect('superadmin')
    return render(request, 'edit_user.html', {'user': user})
def delete_user(request, id):
    user = get_object_or_404(UserMsg, pk=id)
    user.delete()
    return redirect('superadmin')
def mymoney_view(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    try:
        user = UserMsg.objects.get(username=username)
    except UserMsg.DoesNotExist:
        return redirect('login')

    context = {
        'username': username,
        'user': user
    }
    return render(request, 'mymoney.html', context)

def get_balance_api(request):
    username = request.session.get('username')
    if not username:
        return JsonResponse({'error': '未登录'}, status=401)

    try:
        user = UserMsg.objects.get(username=username)
        return JsonResponse({'balance': user.money})
    except UserMsg.DoesNotExist:
        return JsonResponse({'error': '用户不存在'}, status=404)


# 在你的应用目录下的views.py文件中修改index视图


def index(request):
    """首页视图，包含新闻资讯分页功能"""
    # 定义静态新闻数据（模拟数据库查询结果）
    username = request.session.get('username', '用户')
    if request.user.is_authenticated:
        username = request.user.username

    news_data = [
        {
            'id': 1,
            'title': '加快科技创新，亟待金融再发力（财经眼）——加快构建科技金融体制大家谈',
            'source': '环球网',
            'publish_date': '2025-05-07 18:34',
            'url': 'https://finance.sina.com.cn/jjxw/2025-06-16/doc-infafyah3215063.shtml'
        },
        {
            'id': 2,
            'title': '深度解读5月金融数据，谁是社融多增的最大“功臣”',
            'source': '北京商报官方账号',
            'publish_date': '2025-05-07 09:59',
            'url': 'https://news.qq.com/rain/a/20250614A022U600'
        },
        {
            'id': 3,
            'title': '以金融和公用事业为主要配置',
            'source': '南京晨报 ',
            'publish_date': '2025-05-07 16:07',
            'url': 'https://www.msn.cn/zh-cn/news/other/%E4%BB%A5%E9%87%91%E8%9E%8D%E5%92%8C%E5%85%AC%E7%94%A8%E4%BA%8B%E4%B8%9A%E4%B8%BA%E4%B8%BB%E8%A6%81%E9%85%8D%E7%BD%AE/ar-AA1GLpRw?ocid=feedsansarticle'
        },
        {
            'id': 4,
            'title': '王沪宁在两岸融合发展示范区建设专题推进会上强调 高质量建设两岸融合发展示范区',
            'source': '新华社',
            'publish_date': '2025-05-08 15:57',
            'url': 'https://www.financialnews.com.cn/2025-06/16/content_427314.html'
        },
        {
            'id': 5,
            'title': '2025年一季度银行业运行情况分析报告',
            'source': '中国人民银行',
            'publish_date': '2025-04-30 10:20',
            'url': 'https://example.com/news5'
        },
        {
            'id': 6,
            'title': '数字人民币应用场景再拓展，覆盖更多民生领域',
            'source': '经济日报',
            'publish_date': '2025-04-28 14:35',
            'url': 'https://example.com/news6'
        },
        {
            'id': 7,
            'title': '多元金融板块异动拉升，弘业期货涨停',
            'source': '每日经济新闻',
            'publish_date': '2025-04-25 09:10',
            'url': 'https://www.msn.cn/zh-cn/news/other/%E5%A4%9A%E5%85%83%E9%87%91%E8%9E%8D%E6%9D%BF%E5%9D%97%E5%BC%82%E5%8A%A8%E6%8B%89%E5%8D%87-%E5%BC%98%E4%B8%9A%E6%9C%9F%E8%B4%A7%E6%B6%A8%E5%81%9C/ar-AA1GLHJU?ocid=BingNewsLanding&cvid=9985df5ebca944a38b48847ec3e36154&ei=12'
        },
        {
            'id': 8,
            'title': '【开源非银高超团队】关注陆家嘴金融论坛表态，港交所受益于金融开放',
            'source': '市场资讯',
            'publish_date': '2025-04-20 16:42',
            'url': 'https://finance.sina.com.cn/roll/2025-06-15/doc-infaeftf8558079.shtml'
        },
        {
            'id': 9,
            'title': '中国排名前二十的金融学家：思想领航，智启未来 ',
            'source': '人民网',
            'publish_date': '2025-06-16 11:21',
            'url': 'https://www.sohu.com/a/904766945_121261015'
        },
        {
            'id': 10,
            'title': '推动科技和金融“双向奔赴”——四部门详解15项科技金融政策举措',
            'source': '新华社',
            'publish_date': '2025-05-23 07:23 ',
            'url': 'https://www.gov.cn/zhengce/202505/content_7024946.htm'
        }
    ]

    # 分页设置（每页显示3条新闻）
    paginator = Paginator(news_data, 3)
    page = request.GET.get('page')  # 获取URL中的page参数

    try:
        # 获取当前页的新闻数据
        news = paginator.page(page)
    except PageNotAnInteger:
        # 若参数不是整数，显示第一页
        news = paginator.page(1)
    except EmptyPage:
        # 若参数超出范围，显示最后一页
        news = paginator.page(paginator.num_pages)

    context = {
        'username': request.user.username if request.user.is_authenticated else '用户',
        'news': news,
    }
    return render(request, 'index.html', context)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # 为了简化示例，暂时禁用CSRF验证
def verify_password(request):
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        # 这里应该从数据库验证密码，简化示例中我们假设密码是"123456"
        if entered_password == "123456":  # 实际应用中应该从数据库验证
            return JsonResponse({
                'success': True,
                'full_card_number': '1234 5678 9012 3456'  # 实际应用中应该从数据库获取
            })
        else:
            return JsonResponse({
                'success': False
            })
    return JsonResponse({'success': False})
#
# def mymoney_view(request):
#     username = request.session.get('username')
#     if not username:
#         return redirect('login')
#
#     try:
#         user = UserMsg.objects.get(username=username)
#         # 获取最近10条交易记录
#         transactions = Transaction.objects.filter(user=user).order_by('-created_at')[:10]
#
#         context = {
#             'username': username,
#             'user': user,
#             'transactions': transactions
#         }
#         return render(request, 'mymoney.html', context)
#     except UserMsg.DoesNotExist:
#         return redirect('login')
#
#
# def get_balance_api(request):
#     username = request.session.get('username')
#     if not username:
#         return JsonResponse({'error': '未登录'}, status=401)
#
#     try:
#         user = UserMsg.objects.get(username=username)
#         return JsonResponse({
#             'balance': user.money,
#             'updated_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         }, encoder=DjangoJSONEncoder)
#     except UserMsg.DoesNotExist:
#         return JsonResponse({'error': '用户不存在'}, status=404)
#
# def create_transaction(user, transaction_type, amount, description, status='completed', counterparty=None):
#     """
#     创建交易记录
#     :param user: 用户对象
#     :param transaction_type: 交易类型
#     :param amount: 金额(分)
#     :param description: 描述
#     :param status: 状态
#     :param counterparty: 对方信息
#     """
#     transaction = Transaction.objects.create(
#         user=user,
#         transaction_type=transaction_type,
#         amount=amount,
#         description=description,
#         status=status,
#         counterparty=counterparty,
#         transaction_no=f"TX{timezone.now().strftime('%Y%m%d%H%M%S')}{random.randint(1000, 9999)}"
#     )
#     return transaction
#
#
# @login_required
# def add_transaction(request):
#     try:
#         user = UserMsg.objects.get(username=request.session.get('username'))
#     except UserMsg.DoesNotExist:
#         return redirect('login')
#
#     if request.method == 'POST':
#         form = TransactionForm(request.POST)
#         if form.is_valid():
#             transaction = form.save(commit=False)
#             transaction.user = user
#             transaction.save()
#
#             # 更新用户余额
#             if transaction.status == 'completed':
#                 if transaction.transaction_type in ['deposit', 'transfer_in', 'refund', 'interest']:
#                     user.money += transaction.amount
#                 else:
#                     user.money -= transaction.amount
#                 user.save()
#
#             return redirect('mymoney')
#     else:
#         form = TransactionForm()
#
#     return render(request, 'add_transaction.html', {
#         'form': form,
#         'username': user.username
#     })
#
#
# # p1/p1/views.py
# from django.shortcuts import render, redirect
# from .models import UserMsg
# from .forms import TransactionForm
#
#
# def create_transaction(request):
#     if not request.user.is_authenticated:
#         return redirect('login')
#
#     try:
#         user = UserMsg.objects.get(username=request.user.username)
#     except UserMsg.DoesNotExist:
#         return redirect('login')
#
#     if request.method == 'POST':
#         form = TransactionForm(request.POST)
#         if form.is_valid():
#             # 表单保存会触发信号处理
#             transaction = form.save(commit=False)
#             transaction.user = user
#             transaction.save()
#             return redirect('transaction_success')
#     else:
#         form = TransactionForm()
#
#     return render(request, 'transactions/create.html', {'form': form})