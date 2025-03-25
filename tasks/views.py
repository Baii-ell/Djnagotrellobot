from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.core.exceptions import MultipleObjectsReturned
from .models import User, Card, Task
from .serializers import UserSerializer, CardSerializer, TaskSerializer, TaskUpdateSerializer, TaskDeleteSerializer
from rest_framework.views import APIView
from rest_framework.decorators import action


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CardViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer

    def get_queryset(self):
        tg_id = self.request.query_params.get('tg_id')
        
        if not tg_id:
            raise NotFound('Параметр tg_id обязателен для получения списка карточек.')
        try:
            user = User.objects.get(tg_id=tg_id)
        except User.DoesNotExist:
            raise NotFound('Пользователь с указанным tg_id не найден.')
        return Card.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        tg_id = request.data.get('tg_id')
        card_name = request.data.get('name')
        if not tg_id or not card_name:
            return Response(
                {'error': 'Поля tg_id и name являются обязательными.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        phone = request.data.get('phone', '')
        tg_name = request.data.get('tg_name', '')

        user, created = User.objects.get_or_create(
            tg_id=tg_id,
            defaults={'name': tg_name, 'phone': phone}
        )

        card = Card.objects.create(user=user, name=card_name)
        serializer = self.get_serializer(card)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CardDeleteView(APIView):
    def delete(self, request, card_id, *args, **kwargs):
        try:
            card = Card.objects.get(id=card_id)
            card.delete()
            return Response(
                {'message': 'Карточка успешно удалена.'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Card.DoesNotExist:
            return Response(
                {'error': 'Карточка с указанным id не найдена.'},
                status=status.HTTP_404_NOT_FOUND
            )
        




class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
      
        queryset = Task.objects.all()
        card_id = self.kwargs.get('card_id')
        if card_id:
            queryset = queryset.filter(card__id=card_id)
        return queryset
    


    @action(detail=True, methods=['patch'])
    def toggle_done(self, request, pk=None):
        """
        Инвертирует поле done у задачи с переданным id.
        """
        try:
            task = Task.objects.get(id=pk)
            task.done = not task.done  # Инвертируем значение
            task.save()
            serializer = self.get_serializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({'error': 'Задача не найдена'}, status=status.HTTP_404_NOT_FOUND)



    

    def create(self, request, *args, **kwargs):
        tg_id = request.data.get('tg_id')
        card_id = request.data.get('card')
        if not tg_id or not card_id:
            return Response(
                {'error': 'Поля tg_id и card (идентификатор карточки) обязательны.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(tg_id=tg_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'Пользователь с указанным tg_id не найден.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except MultipleObjectsReturned:
            user = User.objects.filter(tg_id=tg_id).first()

        try:
            card = Card.objects.get(id=card_id, user=user)
        except Card.DoesNotExist:
            return Response(
                {'error': 'Карточка не найдена или не принадлежит данному пользователю.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = request.data.copy()
        data.pop('tg_id', None)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(card=card)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    @action(detail=True, methods=['patch'])
    def update_task(self, request, pk=None):
        """
        Обновляет задачу (название, описание и другие поля) по id.
        """
        try:
            task = Task.objects.get(id=pk)
        except Task.DoesNotExist:
            return Response({'error': 'Задача не найдена'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task, data=request.data, partial=True)  # partial=True для частичного обновления
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDeleteView(APIView):
    def delete(self, request, task_id, *args, **kwargs):
        try:
            task = Task.objects.get(id=task_id)
            task.delete()
            return Response(
                {'message': 'Задача успешно удалена.'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Task.DoesNotExist:
            return Response(
                {'error': 'Задача с указанным id не найдена.'},
                status=status.HTTP_404_NOT_FOUND
            )