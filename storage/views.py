from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
import os
from .models import File
from .serializers import FileSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class FileViewSet(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return File.objects.all()
        return File.objects.filter(user=user)

    def perform_create(self, serializer):
        uploaded_file = self.request.FILES.get('file')
        comment = self.request.data.get('comment', '')
        if uploaded_file:
            serializer.save(
                user=self.request.user,
                file=uploaded_file,
                original_name=uploaded_file.name,
                size=uploaded_file.size,
                comment=comment
            )
        else:
            raise ValidationError({'file': 'Файл не был передан.'})

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        name = request.data.get('original_name')
        comment = request.data.get('comment')

        if name:
            instance.original_name = name
        if comment:
            instance.comment = comment

        instance.save()
        return Response(self.get_serializer(instance).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.file.delete(save=False)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], url_path='download')
    def download(self, request, pk=None):
        file_obj = self.get_object()
        file_path = file_obj.file.path
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_obj.original_name)
            return response
        raise Http404

@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Укажите имя пользователя и пароль'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Пользователь уже существует'}, status=status.HTTP_400_BAD_REQUEST)

    User.objects.create_user(username=username, password=password)
    return Response({'message': 'Пользователь создан'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def shared_file(request, uuid):
    try:
        file_obj = File.objects.get(special_link=uuid)
        file_obj.last_download = file_obj.last_download or file_obj.upload_date
        file_obj.save()
        return FileResponse(open(file_obj.file.path, 'rb'), as_attachment=True, filename=file_obj.original_name)
    except File.DoesNotExist:
        raise Http404





