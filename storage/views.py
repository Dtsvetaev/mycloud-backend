import os

from django.contrib.auth.models import User
from django.http import FileResponse, Http404
from rest_framework import generics, status
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import File
from .serializers import FileSerializer, RegisterSerializer, UserSerializer


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

        if not uploaded_file:
            raise ValidationError({'file': 'Файл не был передан.'})

        try:
            serializer.save(
                user=self.request.user,
                file=uploaded_file,
                original_name=uploaded_file.name,
                size=uploaded_file.size,
                comment=comment
            )
        except Exception as e:
            raise ParseError(
                f'Ошибка загрузки файла: {str(e)}'
            )

    @action(detail=True, methods=['get'], url_path='download')
    def download(self, request, pk=None):
        file_obj = self.get_object()
        if file_obj.file and file_obj.file.name:
            response = FileResponse(
                file_obj.file.open('rb'),
                as_attachment=True
            )
            response['Content-Disposition'] = (
                f'attachment; filename="{file_obj.original_name}"'
            )
            return response
        raise Http404


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {"message": "Пользователь успешно зарегистрирован."},
            status=status.HTTP_201_CREATED
        )


class UserManagementViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['post'], url_path='set-admin-status')
    def set_admin_status(self, request, pk=None):
        user = self.get_object()
        user.is_staff = request.data.get('is_staff', False)
        user.is_superuser = request.data.get('is_superuser', False)
        user.save()
        return Response({'status': 'Статус администратора обновлен'})


@api_view(['GET'])
def shared_file(request, uuid):
    try:
        file_obj = File.objects.get(special_link=uuid)
        file_obj.last_download = (
            file_obj.last_download or file_obj.upload_date
        )
        file_obj.save()
        return FileResponse(
            file_obj.file.open('rb'),
            as_attachment=True,
            filename=file_obj.original_name
        )
    except File.DoesNotExist:
        raise Http404
