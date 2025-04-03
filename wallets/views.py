from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from decimal import Decimal

class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    @action(detail=True, methods=['post'])
    def deposit(self, request, pk=None):
    # Deposita um valor na carteira especificada por ID.
    
        wallet = Wallet.objects.get(id=pk)
        amount = request.data.get('amount')

        if amount is None or float(amount) <= 0:
            return Response({'error': 'Valor inválido'}, status=status.HTTP_400_BAD_REQUEST)

        # Converter para Decimal para evitar problemas com float/decimal
        amount_decimal = Decimal(str(amount))
        wallet.balance += amount_decimal
        wallet.save()

        # Para depósitos, considere que a carteira é tanto remetente quanto destinatária
        # ou use uma carteira "sistema" como remetente
        Transaction.objects.create(
            sender=wallet,  # Ou use uma carteira do sistema como remetente
            receiver=wallet,
            amount=amount_decimal
        )

        return Response({'message': 'Depósito realizado com sucesso', 'balance': wallet.balance})

    @action(detail=True, methods=['post'])
    def transfer(self, request, pk=None):
        """
        Transfere um valor da carteira especificada por ID para outra carteira.
        """
        source_wallet = Wallet.objects.get(id=pk)
        destination_id = request.data.get('destination_id')
        amount = request.data.get('amount')

        if amount is None or float(amount) <= 0:
            return Response({'error': 'Valor inválido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            destination_wallet = Wallet.objects.get(id=destination_id)
        except Wallet.DoesNotExist:
            return Response({'error': 'Carteira de destino não encontrada'}, status=status.HTTP_404_NOT_FOUND)

        if source_wallet.balance < float(amount):
            return Response({'error': 'Saldo insuficiente'}, status=status.HTTP_400_BAD_REQUEST)

        # Converter para Decimal
        amount_decimal = Decimal(str(amount))
        source_wallet.balance -= amount_decimal
        destination_wallet.balance += amount_decimal

        source_wallet.save()
        destination_wallet.save()

        # Criar a transação com remetente e destinatário
        Transaction.objects.create(
            sender=source_wallet,
            receiver=destination_wallet,
            amount=amount_decimal
        )

        return Response({'message': 'Transferência realizada com sucesso'})
    
    @action(detail=True, methods=['get'])
    def transactions(self, request, pk=None):
        """
        Lista todas as transferências realizadas de/para a carteira especificada, 
        com filtro opcional por período de data.
        """
        wallet = Wallet.objects.get(id=pk)
        
        # Obter parâmetros de filtragem de data
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        
        # Consulta base para transações de envio ou recebimento
        sent_transactions = Transaction.objects.filter(sender=wallet)
        received_transactions = Transaction.objects.filter(receiver=wallet)
        
        # Aplicar filtros de data, se fornecidos
        if start_date:
            sent_transactions = sent_transactions.filter(timestamp__gte=start_date)
            received_transactions = received_transactions.filter(timestamp__gte=start_date)
        
        if end_date:
            sent_transactions = sent_transactions.filter(timestamp__lte=end_date)
            received_transactions = received_transactions.filter(timestamp__lte=end_date)
        
        # Serializar os resultados
        sent_data = TransactionSerializer(sent_transactions, many=True).data
        received_data = TransactionSerializer(received_transactions, many=True).data
        
        # Adicionar um indicador de tipo para diferenciar transações enviadas e recebidas
        for item in sent_data:
            item['type'] = 'sent'
        
        for item in received_data:
            item['type'] = 'received'
        
        # Combinar os resultados
        all_transactions = list(sent_data) + list(received_data)
        
        # Ordenar por data (mais recente primeiro)
        all_transactions.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return Response(all_transactions)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
