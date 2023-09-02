from django.contrib import admin
from django.urls import path

from .views import ContactsPageView, CoursesPageView, DocSitePageView, LoginPageView, MainPageView, NewsPageView

urlpatterns = [
    path("", MainPageView.as_view()),
    path("login/", LoginPageView.as_view()),
    path("doc_site/", DocSitePageView.as_view()),
    path("contacts/", ContactsPageView.as_view()),
    path("news/", NewsPageView.as_view()),
    path("courses_list/", CoursesPageView.as_view()),
]