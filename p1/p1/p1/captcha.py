import random
import string
from django.http import HttpResponse
from django.core.cache import cache
from PIL import Image, ImageDraw, ImageFont
import io


def generate_captcha(request):
    # 生成4位随机验证码
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

    # 将验证码存入session
    request.session['captcha'] = captcha_text
    request.session.set_expiry(300)  # 5分钟有效期

    # 创建验证码图片
    image = Image.new('RGB', (100, 40), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    try:
        # 尝试使用更漂亮的字体
        font = ImageFont.truetype('arial.ttf', 24)
    except:
        # 如果找不到字体，使用默认字体
        font = ImageFont.load_default()

    # 绘制验证码文本
    draw.text((10, 8), captcha_text, fill=(0, 0, 0), font=font)

    # 添加干扰线
    for _ in range(5):
        draw.line([
            (random.randint(0, 100), random.randint(0, 40)),
            (random.randint(0, 100), random.randint(0, 40))
        ], fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    # 返回图片响应
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    return HttpResponse(buffer.getvalue(), content_type='image/png')