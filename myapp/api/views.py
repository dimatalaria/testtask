
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Transaction, Account
from .serializers import TransactionSerializer, AccountSerializer
from .services import TransactionService


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        account = self.get_object()
        outgoing = account.outgoing_transactions.all()
        incoming = account.incoming_transactions.all()
        data = {
            "incoming": TransactionSerializer(incoming, many=True).data,
            "outgoing": TransactionSerializer(outgoing, many=True).data
        }
        return Response(data)


class TransactionViewSet(viewsets.ViewSet):
    def list(self, request):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        from_account = serializer.validated_data['from_account']
        to_account = serializer.validated_data['to_account']
        amount = serializer.validated_data['amount']

        try:
            transaction = TransactionService.execute_transaction(from_account, to_account, amount)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)


