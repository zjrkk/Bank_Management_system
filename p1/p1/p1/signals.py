# p1/p1/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction, UserMsg


@receiver(post_save, sender=Transaction)
def handle_transaction_update(sender, instance, created, **kwargs):
    """
    交易记录保存后的处理逻辑：
    1. 更新用户余额
    2. 记录审计日志（可选）
    """
    if instance.status == 'completed':
        user = instance.user
        amount = instance.amount  # 注意：这里amount是以分为单位存储的

        try:
            with transaction.atomic():
                # 根据交易类型调整余额
                if instance.transaction_type in ['deposit', 'transfer_in', 'refund', 'interest']:
                    user.money += amount
                else:
                    user.money -= amount

                # 防止余额为负
                if user.money < 0:
                    raise ValueError("账户余额不足")

                user.save()

        except Exception as e:
            # 可以在这里添加错误处理逻辑
            import logging
            logging.error(f"更新用户余额失败: {str(e)}")
            # 可以选择将交易状态标记为失败
            instance.status = 'failed'
            instance.save(update_fields=['status'])