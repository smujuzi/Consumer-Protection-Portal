from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from account.models import Account
from account.decorators import *
from account.forms import AccountUpdateForm
from protect.forms import RepresentativeForm, ComplaintForm
from protect.models import ComplaintModel, FAQ, FAQCategory
from protect.forms import FAQCategoryForm, FAQForm


class FaqsView(View):
    template_name = 'web/faq.html'

    def get(self, request, *args, **kwargs):
        context = {}

        e = FAQCategory.objects.filter(category='Electronic Transactions Act').first()
        i = FAQCategory.objects.filter(category='IT Certification').first()
        q = FAQCategory.objects.filter(category='Quality Assurance').first()
        a1 = FAQCategory.objects.filter(category='Advisory 1').first()
        a2 = FAQCategory.objects.filter(category='Advisory 2').first()

        electronic_transaction_act = FAQ.objects.filter(category=e).first()
        it_certification = FAQ.objects.filter(category=i).first()
        quality_assurance = FAQ.objects.filter(category=q).first()
        advisory_1 = FAQ.objects.filter(category=a1).first()
        advisory_2 = FAQ.objects.filter(category=a2).first()



        context['electronic_transaction_act'] = electronic_transaction_act
        context['it_certification'] = it_certification
        context['quality_assurance'] = quality_assurance
        context['advisory_1'] = advisory_1
        context['advisory_2'] = advisory_2

        if request.user.is_authenticated:
            context['first_name'] = str(request.user.full_names).title().split()[0]

        return render(request, self.template_name, context)


class AddFaqsView(View):
    template_name = 'web/add_faq.html'

    def get(self, request, *args, **kwargs):
        context = {}
        form = FAQCategoryForm()
        context['faq_category_form'] = form
        form = FAQForm()
        context['faq_form'] = form

        if request.user.is_authenticated:
            context['first_name'] = str(request.user.full_names).title().split()[0]

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print("Inside Post")
        context = {}
        faq_category_form = FAQCategoryForm(request.POST)
        faq_form = FAQForm(request.POST)



        new_faq_category = faq_category_form.save()
        category = faq_category_form.cleaned_data.get('category')
        print(category)

        adjust = FAQCategory.objects.filter(category=category).last()
        print("Below Adjust")

        if adjust.category == "Electronic Transactions Act":
            adjust.description = "Frequently Asked Questions (FAQs)" \
                                 " on Electronic Transactions Act, 2011"

        if adjust.category == "IT Certification":
            adjust.description = "Frequently Asked Questions (FAQs)" \
                                 "on Certification Of Providers Of Information " \
                                 "Technology (IT) Products And Services"

        if adjust.category == "Quality Assurance":
            adjust.description = "Frequently Asked Questions (FAQs) for E-Commerce Consumers"

        if adjust.category == "Advisory 1":
            adjust.description = "Advisory on issues that affect the consumer i.e online safety" \
                                 " tips, common scams to avoid, cyber offences, online etiquette, etc"

        if adjust.category == "Advisory 2":
            adjust.description = "Develop content for awareness that will be passed on to the" \
                                 " Communications team to design and produce brochures, pull-out" \
                                 " banners, tear drops, etc. Use infographics, images, etc to" \
                                 " effectively put across the message."

        print("Category and Description")
        print(adjust.category)
        print(adjust.description)
        adjust.save()

        print("Saved!")
        faq_category_form = FAQCategoryForm(request.POST, instance=adjust)
        print("Are we here yet?")

        if faq_category_form.is_valid() & faq_form.is_valid():

            print("Valid!")

            faq_obj = faq_form.save(commit=False)

            print("Are you my problem?")

            faq_category_obj = faq_category_form.save()
            print("Found you!")

            faq_obj.category = faq_category_obj
            print("This is it!")
            faq_obj.save()
            print("The final showdown!")

            return redirect('faq')
        else:
            context['faq_category_form'] = faq_category_form
            context['faq_form'] = faq_form
            return render(request, self.template_name, context)




def view_complaint(request, slug):

    context = {}
    form = AccountUpdateForm(

        initial={
            "email": request.user.email,
            "full_names": request.user.full_names.title(),
            "phone_number": request.user.phone_number,
            "address": request.user.address.title(),
            "image": request.user.image
        }
    )

    context['account_form'] = form

    complaints = get_object_or_404(ComplaintModel, slug=slug)
    context['complaints'] = complaints

    representative = complaints.representative
    context['representative'] = representative

    return render(request, "protect/view_complaint.html", context)



decorators = [login_required(login_url='login')]




@method_decorator(decorators, name='dispatch')
class ComplaintView(View):
    template_name = 'protect/complaint_request.html'

    def get(self, request, *args, **kwargs):

        context = {
            'complaint_form': ComplaintForm(),

            'representative_form': RepresentativeForm(
                initial={
                    "operating_system": "Ubuntu 16.04 LTS",
                    "number_of_cores": "3",
                    "memory": "2Gb",
                    "hdd_space": "100Gb",
                    "partitions": "/home 50Gb, /swap 20Gb, /data 80Gb",
                    "number_of_nics": "2",
                    "connectivity_requirements": "Internet Required, NATed IP address or Public IP and Internet",
                }
            ),
            'account_update_form': AccountUpdateForm(
                initial={
                    "email": request.user.email,
                    "full_names": request.user.full_names,
                    "phone_number": request.user.phone_number,
                    "address": request.user.address,
                    "image": request.user.image
                }
            )
        }

        return render(request, self.template_name, context)

    @staticmethod
    def save_requirements(request, representative_form):#, account_update_form):

        #ALL OLD CODE IS IN COMMENTS

        print("We here")

        #account_update_obj = account_update_form.save(commit=False)
        print("Save completed")

       # account_update_obj.full_names = account_update_form.cleaned_data.get('full_names').title()
        print("Below")

        #print(account_update_obj.full_names)
        #account_update_obj.save()

        representative_obj = representative_form.save(commit=False)
        representative_obj.full_names = representative_form.cleaned_data.get('full_names').title()
        representative_obj.title = representative_form.cleaned_data.get('title').title()
        representative_obj.address = representative_form.cleaned_data.get('address').title()
        representative_obj.save()

        return representative_obj #, account_update_obj

    def post(self, request, *args, **kwargs):

        #ALL OLD CODE IS IN COMMENTS

        print("We in post")
        context = {}
        complaint_form = ComplaintForm(request.POST)
        representative_form = RepresentativeForm(request.POST)
        #account_update_form = AccountUpdateForm(request.POST, instance=request.user)

        if complaint_form.is_valid() and representative_form.is_valid(): #and account_update_form.is_valid():

            complaint_obj = complaint_form.save(commit=False)

            complaint_obj.name_of_respondent = complaint_form.cleaned_data.get('name_of_respondent').title()
            complaint_obj.address = complaint_form.cleaned_data.get('address_of_respondent').title()
            complaint_obj.complainant = request.user

            print("name of respondent")
            print(complaint_obj.name_of_respondent)
            print("address")
            print(complaint_obj.address)


            # representative_obj, account_update_obj = self.save_requirements(
            #     request, representative_form, account_update_form
            # ) Old Code

            representative_obj = self.save_requirements(request, representative_form)


            complaint_obj.representative = representative_obj
            complaint_obj.save()

            return redirect('protect:confirmation', complaint_id=complaint_obj.pk)
        else:
            context['complaint_form'] = complaint_form
            context['representative_form'] = representative_form
            #context['account_update_form'] = account_update_form
            return render(request, self.template_name, context)


class SystemRequirementsView(View):
    template_name = 'protect/system_requirements.html'


    def get(self, request, *args, **kwargs):

        complaint_id = self.kwargs.get('complaint_id')
        print(complaint_id)
        context = {}
        return render(request, self.template_name, context)


class RequestConfirmation(View):
    template_name = 'protect/request_confirmation.html'

    def get(self, request, *args, **kwargs):
        complaint_id = self.kwargs.get('complaint_id')
        context = {}
        if complaint_id:
            complaint = get_object_or_404(ComplaintModel, pk=complaint_id)
            context['complaint'] = complaint
        return render(request, self.template_name, context)


class AssigneeView(View):
    template_name = 'protect/assignee.html'

    def get(self, request, *args, **kwargs):
        complaint_id = self.kwargs.get('complaint_id')
        context = {}
        if complaint_id:
            complaint = get_object_or_404(ComplaintModel, pk=complaint_id)
            context['complaint'] = complaint
        return render(request, self.template_name, context)




