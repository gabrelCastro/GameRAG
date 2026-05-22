import logging

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from chat.application.chat_service import ChatService
from games.interfaces.serializers import GameSerializer

logger = logging.getLogger(__name__)


class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        message = request.data.get('message', '').strip()
        if not message:
            return Response({'error': 'O campo "message" é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = ChatService().answer(message)
        except Exception:
            logger.exception('Erro ao processar mensagem do chat')
            return Response({'error': 'Erro interno ao processar sua mensagem.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'answer': result['answer'],
            'games': GameSerializer(result['games'], many=True).data,
        })
