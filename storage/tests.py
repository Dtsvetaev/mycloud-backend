from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from storage.models import File


class FileStorageAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123')
        self.client = APIClient()

        # Получаем JWT токен
        response = self.client.post(
            '/api/token/', {'username': 'testuser', 'password': 'testpass123'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_file_upload(self):
        file = SimpleUploadedFile(
            "testfile.txt", b"hello world", content_type="text/plain")
        response = self.client.post("/api/files/", {"file": file})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(File.objects.count(), 1)

    def test_file_list(self):
        file = SimpleUploadedFile(
            "list.txt", b"list content", content_type="text/plain")
        self.client.post("/api/files/", {"file": file})
        response = self.client.get("/api/files/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_file_download(self):
        test_file = SimpleUploadedFile(
            "download.txt", b"download content", content_type="text/plain")
        upload_response = self.client.post("/api/files/", {"file": test_file})
        self.assertEqual(upload_response.status_code, status.HTTP_201_CREATED)

        file_id = upload_response.data["id"]
        response = self.client.get(f"/api/files/{file_id}/download/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Content-Disposition', response)

    def test_special_link_download(self):
        test_file = SimpleUploadedFile(
            "link.txt", b"link content", content_type="text/plain")
        upload_response = self.client.post("/api/files/", {"file": test_file})
        self.assertEqual(upload_response.status_code, status.HTTP_201_CREATED)

        file_id = upload_response.data["id"]
        file_obj = File.objects.get(id=file_id)

        response = self.client.get(
            f"/api/files/shared/{file_obj.special_link}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Content-Disposition', response)
