import pickle
from http import HTTPStatus
from unittest import mock

from django.test import TestCase, Client
from django.urls import reverse

from authapp.models import CustomUser
from mainapp.models import News, Courses
from mainapp.tasks import send_feedback_mail
from django.core import mail as django_mail


class TestMainPage(TestCase):
    def test_page_open(self):
        path = reverse("mainapp:main")
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)


class TestNewsPage(TestCase):
    fixtures = (
        "authapp/fixtures/001_user_admin.json",
        "mainapp/fixtures/001_news.json",
        "authapp/fixtures/001_auth.json",
    )

    def setUp(self):
        super().setUp()
        self.client_with_auth = Client()
        path_auth = reverse("authapp:login")
        self.client_with_auth.post(path_auth, data={"username": "admin", "password": "admin"})

    def test_page_open_list(self):
        path = reverse("mainapp:news")
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_open_detail(self):
        news_obj = News.objects.first()
        path = reverse("mainapp:news_detail", args=[news_obj.pk])
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_open_create_deny_access(self):
        path = reverse("mainapp:news_create")
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_page_open_create_by_admin(self):
        path = reverse("mainapp:news_create")
        result = self.client_with_auth.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_create_in_web(self):
        counter_before = News.objects.count()
        path = reverse("mainapp:news_create")
        self.client_with_auth.post(
            path,
            data={
                "title": "NewTestNews001",
                "preambule": "NewTestNews001",
                "body": "NewTestNews001",
            },
        )
        self.assertGreater(News.objects.count(), counter_before)

    def test_page_open_update_deny_access(self):
        news_obj = News.objects.first()
        path = reverse("mainapp:news_update", args=[news_obj.pk])
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_page_open_update_by_admin(self):
        news_obj = News.objects.first()
        path = reverse("mainapp:news_update", args=[news_obj.pk])
        result = self.client_with_auth.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_update_in_web(self):
        new_title = "NewTestTitle001"
        news_obj = News.objects.first()
        self.assertNotEqual(news_obj.title, new_title)
        path = reverse("mainapp:news_update", args=[news_obj.pk])
        result = self.client_with_auth.post(
            path,
            data={
                "title": new_title,
                "preamble": news_obj.preamble,
                "body": news_obj.body,
            },
        )
        self.assertEqual(result.status_code, HTTPStatus.FOUND)
        news_obj.refresh_from_db()
        self.assertEqual(news_obj.title, new_title)

    def test_delete_deny_access(self):
        news_obj = News.objects.first()
        path = reverse("mainapp:news_delete", args=[news_obj.pk])
        result = self.client.post(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_delete_in_web(self):
        news_obj = News.objects.first()
        path = reverse("mainapp:news_delete", args=[news_obj.pk])
        self.client_with_auth.post(path)
        news_obj.refresh_from_db()
        self.assertTrue(news_obj.deleted)


class TestTaskMailSend(TestCase):
    fixtures = (
        "authapp/fixtures/001_user_admin.json",
        "authapp/fixtures/001_auth.json",
    )

    def test_mail_send(self):
        message_text = "test_message_text"
        user_obj = CustomUser.objects.first()
        send_feedback_mail(
            {
                "user_id": user_obj.id,
                "message": message_text
            }
        )
        self.assertEqual(django_mail.outbox[0].body, message_text)


# class TestCoursesWithMock(TestCase):
#     fixtures = (
#         "authapp/fixtures/001_user_admin.json",
#         "authapp/fixtures/001_auth.json",
#         "mainapp/fixtures/002_courses.json",
#         "mainapp/fixtures/003_lessons.json",
#         "mainapp/fixtures/004_teachers.json",
#     )
#
#     def test_page_open_detail(self):
#         course_obj = Courses.objects.get(pk=2)
#         path = reverse("mainapp:courses_detail", args=[course_obj.pk])
#         with open(
#             "mainapp/fixtures/006_feedback_list_2.bin", "rb"
#         ) as inpf, mock.patch("django.core.cache.cache.get") as mocked_cache:
#             mocked_cache.return_value = pickle.load(inpf)
#             result = self.client.get(path)
#             self.assertEqual(result.status_code, HTTPStatus.OK)
#             self.assertTrue(mocked_cache.called)
