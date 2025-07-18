from django.db import transaction as db_transaction

from .models import Transaction


class TransactionService:
    @staticmethod
    def execute_transaction(from_account, to_account, amount):
        with db_transaction.atomic():
            from_account.refresh_from_db()
            to_account.refresh_from_db()

            if from_account.balance < amount:
                raise ValueError("Недостаточно средств")

            from_account.balance -= amount
            to_account.balance += amount

            from_account.save()
            to_account.save()

            return Transaction.objects.create(
                from_account=from_account,
                to_account=to_account,
                amount=amount
            )