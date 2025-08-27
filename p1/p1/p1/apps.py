# p1/p1/apps.py
from django.apps import AppConfig

class P1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'p1'

    def ready(self):
        # 注册信号处理器
        import p1.signals  # 确保信号被注册