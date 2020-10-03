from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from protect.models import ComplaintModel
from django.utils.decorators import method_decorator

from .models import *


class HomePageView(View):
    template_name = 'web/home-page.html'

    def get(self, request, *args, **kwargs):
        context = {}
        if request.user.is_authenticated:
            context['first_name'] = str(request.user.full_names).title().split()[0]
        return render(request, self.template_name, context)


class AboutUsView(View):
    template_name = 'web/about.html'

    def get(self, request, *args, **kwargs):
        context = {}
        if request.user.is_authenticated:
            context['first_name'] = str(request.user.full_names).title().split()[0]
        return render(request, self.template_name, context)


class ConsumerProtectionView(View):
    template_name = 'web/data-protection.html'

    def get(self, request, *args, **kwargs):
        context = {}
        if request.user.is_authenticated:
            context['first_name'] = str(request.user.full_names).title().split()[0]
        return render(request, self.template_name, context)


class ResourcesView(View):
    template_name = 'web/resources.html'

    def get(self, request, *args, **kwargs):
        context = {}
        if request.user.is_authenticated:
            context['first_name'] = str(request.user.full_names).title().split()[0]
        return render(request, self.template_name, context)


class OpportunitiesView(View):
    template_name = 'web/opportunities.html'

    def get(self, request, *args, **kwargs):
        context = {}
        if request.user.is_authenticated:
            context['first_name'] = str(request.user.full_names).title().split()[0]
        return render(request, self.template_name, context)


class ContactUsView(View):
    template_name = 'web/contact-us.html'

    def get(self, request, *args, **kwargs):
        context = {}
        if request.user.is_authenticated:
            context['first_name'] = str(request.user.full_names).title().split()[0]
        return render(request, self.template_name, context)



