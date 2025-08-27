from django.utils import timezone
import random
from .models import Transaction, UserMsg


def create_transaction(user_id, transaction_type, amount_in_yuan, description,
                       status='completed', counterparty=None, counterparty_account=None):
    """
    创建交易记录的工具函数
    :param user_id: 用户ID
    :param transaction_type: 交易类型
    :param amount_in_yuan: 金额(元)
    :param description: 描述
    :param status: 状态
    :param counterparty: 对方名称
    :param counterparty_account: 对方账号
    :return: Transaction对象
    """
    try:
        user = UserMsg.objects.get(id=user_id)
        amount = int(amount_in_yuan * 100)  # 转换为分

        transaction = Transaction.objects.create(
            user=user,
            transaction_type=transaction_type,
            amount=amount,
            description=description,
            status=status,
            counterparty=counterparty,
            counterparty_account=counterparty_account
        )

        # 更新用户余额
        if status == 'completed':
            if transaction_type in ['deposit', 'transfer_in', 'refund', 'interest']:
                user.money += amount
            else:
                user.money -= amount
            user.save()

        return transaction
    except UserMsg.DoesNotExist:
        raise ValueError("用户不存在")