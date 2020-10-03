from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import login, authenticate, logout

from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm, StaffRegistrationForm
from django.utils.decorators import method_decorator
from django.views import View

from account.models import Account
from protect.models import ComplaintModel
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from .decorators import *


@login_required(login_url='login')
@admin_redirect
def home_screen_view(request):
    context = {}
    template_name = "account/mda_home.html"
    complaints = ComplaintModel.objects.filter(complainant=request.user).order_by('date_of_request')
    pending_complaints = ComplaintModel.objects.filter(complainant=request.user, status='Pending').order_by(
        'date_of_request')
    action_taken = ComplaintModel.objects.filter(complainant=request.user, status='Complete').order_by(
        'date_of_request')
    context['complaints'] = complaints
    context['pending_complaints'] = pending_complaints
    context['action_taken'] = action_taken
    if request.user.is_authenticated:
        print("User name = ")
        print(request.user.full_names)
        context['first_name'] = str(request.user.full_names).title().split()[0]
    return render(request, template_name, context)


def logout_view(request):
    logout(request)
    return redirect('/')


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("home")

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    # print(form)
    return render(request, "account/login.html", context)


def account_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "email": request.POST['email'],
                "full_names": request.POST['full_names'],
                "phone_number": request.POST['phone_number'],
                "address": request.POST['address'],
                "image": request.POST['image'],
            }
            account = form.save(commit=False)
            account.full_names = str(form.cleaned_data.get('full_names')).title()
            account.address = str(form.cleaned_data.get('address')).title()
            account.save()
            context['success_message'] = "Updated"
    else:
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
        complaints = ComplaintModel.objects.filter(complainant=request.user).order_by('date_of_request')
        context['complaints'] = complaints

    return render(request, "account/account.html", context)





def must_authenticate_view(request):
    return render(request, 'account/must_authenticate.html', {})


class ViewUser(View):
    template_name = 'account/display_users.html'

    def get(self, request, *args, **kwargs):
        context = {}

        accounts = Account.objects.all()
        context['accounts'] = accounts

        return render(request, self.template_name, context)


class RegisterView(View):
    template_name = 'account/register.html'


    def get(self, request, *args, **kwargs):

        context = {}
        form = RegistrationForm()
        context['registration_form'] = form
        return render(request, self.template_name, context)

    @staticmethod
    def create_institution(request, company_form):
        email = company_form.cleaned_data.get('email')
        raw_password = company_form.cleaned_data.get('password1')
        account = authenticate(email=email, password=raw_password)
        login(request, account)
        company_form.save()
        return redirect('user')

    def post(self, request, *args, **kwargs):
        print("Inside Post")
        context = {}
        company_form = RegistrationForm(request.POST)
        if company_form.is_valid():
            company_form.save()
            email = company_form.cleaned_data.get('email')
            raw_password = company_form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('user')
        else:
            context['registration_form'] = company_form
            return render(request, self.template_name, context)


def registration_view(request):
    print("Inside Registration View")
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('user')
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)



# STAFF REGISTRATION


class StaffRegisterView(View):
    template_name = 'account/register_staff.html'

    def get(self, request, *args, **kwargs):
        print("GET")
        context = {}
        form = StaffRegistrationForm()
        context['registration_form'] = form
        return render(request, self.template_name, context)

    @staticmethod
    def create_institution(request, company_form):
        print("Inside Create_Institution")
        email = company_form.cleaned_data.get('email')
        raw_password = company_form.cleaned_data.get('password1')
        account = authenticate(email=email, password=raw_password)
        login(request, account)
        company_form.save()
        return redirect('user')

    def post(self, request, *args, **kwargs):
        print("Inside Post")
        context = {}
        company_form = StaffRegistrationForm(request.POST)

        new_account = company_form.save()
        email = company_form.cleaned_data.get('email')
        print(email)

        adjust = Account.objects.get(email=email)
        adjust.is_staff = True

        if adjust.role == "Manager":
            adjust.is_admin = True

        print(adjust.role)
        adjust.save()

        company_form = StaffRegistrationForm(request.POST, instance=adjust)

        if company_form.is_valid():
            company_form.save()

            email = company_form.cleaned_data.get('email')
            raw_password = company_form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('user')
        else:
            context['registration_form'] = company_form
            return render(request, self.template_name, context)


def staff_registration_view(request):
    print("Inside Staff Registration View")
    context = {}
    if request.POST:
        form = StaffRegistrationForm(request.POST)



        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('user')
        else:
            context['registration_form'] = form

    else:
        form = StaffRegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register_staff.html', context)
# STAFF REGISTRATION


decorators = [login_required(login_url='login')]


@method_decorator(decorators, 'dispatch')
class AdminView(View):
    template_name = 'account/admin_home.html'

    def get(self, request, *args, **kwargs):
        context = {}

        complaints = ComplaintModel.objects.filter(complainant__role='complainant').order_by('date_of_request')
        pending_complaints = ComplaintModel.objects.filter(status='Pending').order_by('date_of_request')
        actioned = ComplaintModel.objects.filter(status='Complete').order_by('date_of_request')
        complainants = Account.objects.filter(role='complainant')
        staff_members = Account.objects.filter(is_staff=True)
        handle_complaints = ComplaintModel.objects.filter(implemented_by=request.user).order_by('date_of_request')

        context['complaints'] = complaints
        context['pending_complaints'] = pending_complaints
        context['actioned'] = actioned
        context['complainants'] = complainants
        context['staff_members'] = staff_members
        context['handle_complaints'] = handle_complaints

        if request.user.is_authenticated:
            context['first_name'] = str(request.user.full_names).title().split()[0]

        return render(request, self.template_name, context)

class HandleView(View):
    template_name = 'account/handle_complaint.html'
    print("We made it!")

    def get(self, request, slug, *args, **kwargs):
        context = {}
        print("We in get")

        selected_complaint = get_object_or_404(ComplaintModel, slug=slug)
        print(selected_complaint)

        selected_complaint.status = 'Complete'
        selected_complaint.save()

        context['selected_complaint'] = selected_complaint

        return render(request, self.template_name, context)


def handle_complaint(request):
    context = {}
    print("Inside Handle Complaint")

    return render(request, "account/handle_complaint.html", context)


def delegate_complaint(request, slug):

    context = {}

    staff_members = Account.objects.filter(is_staff=True)
    context['staff_members'] = staff_members

    selected_complaint = get_object_or_404(ComplaintModel, slug=slug)
    print(selected_complaint)
    context['selected_complaint'] = selected_complaint

    return render(request, "account/delegate.html", context)







def assign(request, selected_complaint=None, staff_member=None):
    context = {}

    print("Inside Assign")

    staff_member = Account.objects.filter(pk=staff_member).first()

    selected_complaint = ComplaintModel.objects.filter(slug=selected_complaint).first()

    print(staff_member.email)


    print("Complaint Title:")
    print(selected_complaint.address_of_respondent)

    selected_complaint.implemented_by = staff_member
    selected_complaint.status = 'Under Review'

    context['selected_complaint'] = selected_complaint

    return render(request, "account/admin_home.html", context)


class DelegateComplaint(View):

    def get(self, request, *args, **kwargs):

        context = {}
        print("In here!")

        staff_m = kwargs.get('staff_member')
        print("staff_m")
        print(staff_m)

        selected_c = kwargs.get('selected_complaint')
        print("selected_c")
        print(selected_c)

        staff_member = Account.objects.filter(pk=staff_m).first()

        selected_complaint = ComplaintModel.objects.filter(pk=selected_c).first()

        print(staff_member.email)

        print("Complaint Title:")
        print(selected_complaint.title)

        selected_complaint.implemented_by = staff_member
        selected_complaint.status = 'Under Review'

        print("Implemented by")
        print(selected_complaint.implemented_by.email)

        print("Status")
        print(selected_complaint.status)

        selected_complaint.save()

        return redirect('admin_home')

    def assign(request, selected_complaint=None, staff_member=None):
        context = {}

        print("Inside Assign")

        staff_member = Account.objects.filter(pk=staff_member).first()

        selected_complaint = ComplaintModel.objects.filter(slug=selected_complaint).first()

        print(staff_member.email)

        print("Complaint Title:")
        print(selected_complaint.address_of_respondent)

        selected_complaint.implemented_by = staff_member
        selected_complaint.status = 'Under Review'

        context['selected_complaint'] = selected_complaint

        return render(request, "account/admin_home.html", context)



