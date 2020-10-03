from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from .views import *



from protect.views import (

    ComplaintView,
    SystemRequirementsView,
    AssigneeView,
    RequestConfirmation,
    view_complaint,

)

app_name = 'protect'

urlpatterns = [
    path('complaint/', ComplaintView.as_view(), name='complaint'),
    path('requirements/', SystemRequirementsView.as_view(), name='requirements'),
    path('confirmation/<int:complaint_id>/', RequestConfirmation.as_view(), name='confirmation'),
    path('<slug>', view_complaint, name="view_complaint"),

]