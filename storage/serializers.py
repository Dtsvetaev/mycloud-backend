from rest_framework import serializers
from .models import File

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'user', 'file', 'original_name', 'comment', 'size', 'upload_date', 'last_download', 'special_link')
        read_only_fields = ('id', 'user', 'original_name', 'size', 'upload_date', 'last_download', 'special_link')




