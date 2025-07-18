from rest_framework import serializers

from .models import Account, Transaction


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('created_at',)

    def validate(self, data):
        if data['from_account'] == data['to_account']:
            raise serializers.ValidationError("Нельзя перевести средства самому себе.")
        if data['amount'] <= 0:
            raise serializers.ValidationError("Сумма перевода должна быть положительной.")
        if data['from_account'].balance < data['amount']:
            raise serializers.ValidationError("Недостаточно средств на счете отправителя.")
        return data