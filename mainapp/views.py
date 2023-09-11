from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotFound

from mainapp.models import News, Courses, Lesson, CourseTeachers


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"


class NewsPageView(TemplateView):
    template_name = "mainapp/news.html"
    paginated_by = 3

    def get_context_data(self, **kwargs):

        page_number = self.request.GET.get('page', 1)
        paginator = Paginator(News.objects.all(), self.paginated_by)
        page = paginator.get_page(page_number)
        context = super().get_context_data(**kwargs)

        context['page'] = page

        return context


class NewsDetailsPageView(TemplateView):
    template_name = 'mainapp/news_details.html'

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_object'] = get_object_or_404(News, pk=pk)
        return context


class LoginPageView(TemplateView):
    template_name = "mainapp/login.html"


class ContactsPageView(TemplateView):
    template_name = "mainapp/contacts.html"


class DocSitePageView(TemplateView):
    template_name = "mainapp/doc_site.html"


class CoursesPageView(TemplateView):
    template_name = "mainapp/courses_list.html"
    paginated_by = 3

    def get_context_data(self, **kwargs):

        page_number = self.request.GET.get('page', 1)
        paginator = Paginator(Courses.objects.all(), self.paginated_by)
        page = paginator.get_page(page_number)
        context = super().get_context_data(**kwargs)

        context['page'] = page

        return context


class CoursesDetailView(TemplateView):
    template_name = "mainapp/courses_detail.html"

    def get_context_data(self, pk=None, **kwargs):
        context = super(CoursesDetailView, self).get_context_data(**kwargs)
        context["course_object"] = get_object_or_404(Courses, pk=pk)
        context["lessons"] = Lesson.objects.filter(course=context["course_object"])
        context["teachers"] = CourseTeachers.objects.filter(course=context["course_object"])

        return context
