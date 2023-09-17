from django.contrib import admin
from django.urls import path

from .views import (ContactsPageView,
                    DocSitePageView,
                    MainPageView,
                    CoursesDetailView,
                    NewsCreateView,
                    NewsUpdateView,
                    NewsDetailView,
                    NewsListView,
                    NewsDeleteView, CoursesListView, CourseFeedbackFormProcessView)
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path("", MainPageView.as_view(), name='main'),
    path("news/", NewsListView.as_view(), name='news'),
    path("news/create/", NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/detail', NewsDetailView.as_view(), name='news_detail'),
    path('news/<int:pk>/update', NewsUpdateView.as_view(), name='news_update'),
    path('news/<int:pk>/delete', NewsDeleteView.as_view(), name='news_delete'),

    path("courses/", CoursesListView.as_view(), name="courses"),
    path("courses/<int:pk>/", CoursesDetailView.as_view(), name="courses_detail"),
    path("course_feedback/", CourseFeedbackFormProcessView.as_view(), name="course_feedback"),

    path("contacts/", ContactsPageView.as_view(), name='contacts'),
    path("doc_site/", DocSitePageView.as_view(), name='docs'),
]
