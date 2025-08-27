from django import template
from django.utils.safestring import mark_safe
register = template.Library()   #register的名字是固定的,不可改变

# 利用装饰器 @register.filter 自定义过滤器。
# 注意：装饰器的参数最多只能有 2 个。
@register.filter
def my_filter(v1, v2):
    return v1 * v2

#利用装饰器 @register.simple_tag 自定义标签。
@register.simple_tag
def my_tag1(v1, v2, v3):
    return v1 * v2 * v3

# 定义标签时，用上 mark_safe 方法，令标签语义化，相当于 jQuery 中的 html() 方法。
# 和前端HTML文件中的过滤器 safe 效果一样。
@register.simple_tag
def my_html(v1, v2):
    temp_html = "<input type='text' id='%s' class='%s' />" %(v1, v2)
    return mark_safe(temp_html)