from django.contrib import admin
from django.urls import path

from .views import (ContactsPageView, CoursesPageView, DocSitePageView, LoginPageView, MainPageView, NewsPageView,
                    NewsDetailsPageView, CoursesDetailView)
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path("", MainPageView.as_view(), name='main'),
    path("login/", LoginPageView.as_view(), name='login'),
    path("doc_site/", DocSitePageView.as_view(), name='docs'),
    path("contacts/", ContactsPageView.as_view(), name='contacts'),
    path("news/", NewsPageView.as_view(), name='news'),
    path("news/<int:pk>", NewsDetailsPageView.as_view(), name='news_details'),
    path("courses_list/", CoursesPageView.as_view(), name='courses'),
    path('course/<int:pk>/', CoursesDetailView.as_view(), name='course_details')
]
