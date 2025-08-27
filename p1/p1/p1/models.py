from django.db import models
from django.utils import timezone

from django.db import models
from django.utils import timezone
import uuid
class Xue_Xi_Biao(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Xue_Xi_Biao'


class UserMsg(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    cardid = models.CharField(max_length=50)
    money = models.IntegerField(default=0)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'UserMsg'


from django.db import models
from django.utils import timezone
import random


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', '存款'),
        ('withdraw', '取款'),
        ('transfer_in', '转账收入'),
        ('transfer_out', '转账支出'),
        ('payment', '支付'),
        ('refund', '退款'),
        ('interest', '利息'),
        ('other', '其他'),
    )

    STATUS_CHOICES = (
        ('pending', '处理中'),
        ('completed', '已完成'),
        ('failed', '失败'),
        ('cancelled', '已取消'),
    )

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserMsg', on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.IntegerField()  # 以分为单位
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    counterparty = models.CharField(max_length=100, blank=True, null=True)
    counterparty_account = models.CharField(max_length=50, blank=True, null=True)
    transaction_no = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'Transaction'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['transaction_no']),
        ]

    def save(self, *args, **kwargs):
        if not self.pk:  # 新建记录时生成交易号
            self.transaction_no = self._generate_transaction_no()
        super().save(*args, **kwargs)

    def _generate_transaction_no(self):
        return f"TX{timezone.now().strftime('%Y%m%d%H%M%S')}{random.randint(1000, 9999)}"

    @property
    def amount_display(self):
        """返回以元为单位的金额"""
        return f"{self.amount / 100:.2f}"

    # 在你的应用目录下的models.py文件中添加以下内容



    class NewsArticle(models.Model):
        """新闻文章模型"""
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        title = models.CharField(max_length=200, verbose_name="新闻标题")
        content = models.TextField(verbose_name="新闻内容")
        source = models.CharField(max_length=100, verbose_name="新闻来源")
        publish_date = models.DateTimeField(default=timezone.now, verbose_name="发布日期")
        url = models.URLField(verbose_name="原文链接", blank=True, null=True)

        class Meta:
            verbose_name = "新闻文章"
            verbose_name_plural = "新闻文章"
            ordering = ["-publish_date"]  # 按发布日期降序排列

        def __str__(self):
            return self.title
