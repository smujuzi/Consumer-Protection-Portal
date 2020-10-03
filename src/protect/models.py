from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils.text import slugify
from .config import *


class RepresentativeModel(models.Model):
    representative_id = models.AutoField(primary_key=True)
    full_names = models.CharField(max_length=100, null=False, blank=False)
    title = models.CharField(max_length=100, null=False, blank=False)
    address = models.CharField(max_length=200, null=False, blank=False)
    email_address = models.EmailField(max_length=100, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    relationship_to_complainant = models.CharField(max_length=100, null=True, blank=False)

    class Meta:
        verbose_name = 'Representative'
        verbose_name_plural = 'Representative'

    def __str__(self):
        return self.full_names


class ComplaintModel(models.Model):
    complaint_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=False, blank=False)
    name_of_respondent = models.CharField(max_length=100, null=False, blank=False)
    address_of_respondent = models.CharField(max_length=200, blank=False, null=False)
    dpo_contacted = models.CharField(max_length=200, blank=False, null=False)

    details_of_complaint = models.TextField(max_length=500, null=True, blank=True)
    complainant = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE)
    representative = models.ForeignKey(RepresentativeModel, null=True, on_delete=models.SET_NULL)

    date_serviced = models.DateTimeField(null=True, blank=True, verbose_name="date_received")
    status = models.CharField(max_length=200, blank=False, null=False, default='Pending')
    date_implemented = models.DateTimeField(null=True, blank=True, verbose_name="date_implemented")
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_by', blank=True,
                                    on_delete=models.SET_NULL, null=True)
    implemented_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='implemented_by', blank=True,
                                       on_delete=models.SET_NULL, null=True)

    date_of_request = models.DateTimeField(auto_now_add=True, verbose_name="request date")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        verbose_name = 'Complaint'
        verbose_name_plural = 'Complaints'

    def __str__(self):
        return self.slug


def pre_save_host_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name_of_respondent + "-" + instance.title)


pre_save.connect(pre_save_host_receiver, sender=ComplaintModel)


class DataControllerModel(models.Model):
    full_names = models.CharField(max_length=100, null=False, blank=False)
    address = models.CharField(max_length=200, null=False, blank=False)
    email_address = models.EmailField(max_length=100, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    data_protection_officer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='data_officer_contacted',
                                                blank=True,
                                                on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Data Controller'
        verbose_name_plural = 'Data Controllers'

    def __str__(self):
        return self.full_names


class RemedialMeasuresModel(models.Model):
    measures_taken = models.TextField(max_length=500, null=True, blank=True)
    has_notified_regulators = models.CharField(max_length=200, null=False, blank=False, choices=YES_NO)
    regulators_notified = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        verbose_name = 'Remedial Measure'
        verbose_name_plural = 'Remedial Measures'

    def __str__(self):
        return str(self.measures_taken)[:8]


class DataBreachModel(models.Model):
    data_breach_id = models.AutoField(primary_key=True)
    nature = models.CharField(max_length=100, null=False, blank=False)
    date_of_awareness = models.DateField(null=True, blank=True, verbose_name="date_of_awareness")
    subject_personal_data = models.CharField(max_length=100, null=False, blank=False)
    personal_data_categories = models.CharField(max_length=100, null=False, blank=False)
    number_of_subjects = models.CharField(max_length=100, null=False, blank=False)

    details = models.TextField(max_length=500, null=True, blank=True)
    risk_of_harm = models.TextField(max_length=500, null=True, blank=True)
    representative = models.ForeignKey(RepresentativeModel, null=True, on_delete=models.SET_NULL)
    measures = models.ForeignKey(RemedialMeasuresModel, null=True, on_delete=models.SET_NULL)

    date_serviced = models.DateTimeField(null=True, blank=True, verbose_name="date_received")
    date_implemented = models.DateTimeField(null=True, blank=True, verbose_name="date_implemented")
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='breach_approved_by', blank=True,
                                    on_delete=models.SET_NULL, null=True)
    implemented_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='breach_implemented_by', blank=True,
                                       on_delete=models.SET_NULL, null=True)

    date_of_request = models.DateTimeField(auto_now_add=True, verbose_name="request date")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        verbose_name = 'Data Breach'
        verbose_name_plural = 'Data Breaches'

    def __str__(self):
        return self.nature


def pre_save_breach_receiver(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.nature)


pre_save.connect(pre_save_breach_receiver, sender=DataBreachModel)


class FAQCategory(models.Model):
    """
    Quality Assurance, IT certification, Electronic Transactions Act, Advisory 1, Advisory 2

    """

    category = models.CharField(max_length=500, null=False, blank=False)
    description = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.category


class FAQ(models.Model):
    id = models.AutoField(primary_key=True)
    subtitle = models.TextField(null=False, blank=False)
    question = models.CharField(max_length=1000, null=False, blank=False)
    answer = models.TextField(null=False, blank=False)
    category = models.ForeignKey(FAQCategory, null=True, blank=False, on_delete=models.SET_NULL)
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

