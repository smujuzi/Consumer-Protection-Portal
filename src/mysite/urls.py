"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf.urls import url
from django.conf import settings

from account import views

from account.views import (
    staff_registration_view,
    registration_view,
    logout_view,
    login_view,
    account_view,
    home_screen_view,
    must_authenticate_view,
    RegisterView,
    StaffRegisterView,
    AdminView,
    ViewUser,
    delegate_complaint,
    DelegateComplaint,
    handle_complaint,
    HandleView,



)
from web.views import (
    HomePageView, AboutUsView,
    ConsumerProtectionView,
    ResourcesView,
    OpportunitiesView,
    ContactUsView,



)

from protect.views import (

    ComplaintView,
    SystemRequirementsView,
    AssigneeView,
    RequestConfirmation,
    view_complaint,
    FaqsView,
    AddFaqsView,
)

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('user/', home_screen_view, name="user"),
    path('account/', account_view, name="account"),
    path('admin/', admin.site.urls),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('must_authenticate/', must_authenticate_view, name="must_authenticate"),
    path('register/', RegisterView.as_view(), name="register"),
    path('register_staff/', StaffRegisterView.as_view(), name="register_staff"),
    path('home/', AdminView.as_view(), name="admin_home"),
    path('action/<slug>/', HandleView.as_view(), name="handle"),
    path('delegate/<slug>/', delegate_complaint, name="delegate"),
    path('faqs/', FaqsView.as_view(), name="faqs"),
    path('display_users/', ViewUser.as_view(), name="display_users"),
    path('handle_complaint', handle_complaint, name="handle_complaint"),
    url(r'^assign/(?P<selected_complaint>\w+)/(?P<staff_member>\w+)/$', DelegateComplaint.as_view(), name='assign'),

    # Protect
    path('protect/', include('protect.urls', 'protect')),
    path('complaint/', ComplaintView.as_view(), name='complaint'),
    path('requirements/', SystemRequirementsView.as_view(), name='requirements'),
    path('confirmation/<int:complaint_id>/', RequestConfirmation.as_view(), name='confirmation'),
    path('<slug>', view_complaint, name="view_complaint"),
    path('faq/', FaqsView.as_view(), name='faq'),
    path('add_faq/', AddFaqsView.as_view(), name='add_faq'),

    # Web
    path('about/', AboutUsView.as_view(), name='about'),
    path('consumer/protection/', ConsumerProtectionView.as_view(), name='protection'),
    path('resources/', ResourcesView.as_view(), name='resources'),
    path('opportunities/', OpportunitiesView.as_view(), name='opportunities'),
    path('contact-us/', ContactUsView.as_view(), name='contact'),



    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
         name='password_change'),

    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
