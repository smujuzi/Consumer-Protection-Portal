from django import forms
from material import Layout, Row, Fieldset
from .models import *
from .config import *
from protect.models import FAQCategory, FAQ

CATEGORY_CHOICES = (
    ("Electronic Transactions Act", 'Electronic Transactions Act'),
    ("IT Certification", 'IT Certification'),
    ("Quality Assurance", 'Quality Assurance'),
    ("Advisory 1", 'Advisory 1'),
    ("Advisory 2", 'Advisory 2'),
)


class FAQCategoryForm(forms.ModelForm):
    category = forms.ChoiceField(label='Category', choices=CATEGORY_CHOICES)

    class Meta:
        model = FAQCategory
        fields = ['category']

    layout = Layout('category')


class FAQForm(forms.ModelForm):
    subtitle = forms.CharField(label='Subtitle',
                               widget=forms.TextInput(
                                   attrs={'placeholder': 'Write the answer to your question'}))
    question = forms.CharField(label='Question',
                               widget=forms.TextInput(attrs={'placeholder': 'Ask something...'}))
    answer = forms.CharField(label='Answer',
                             widget=forms.TextInput(
                                 attrs={'cols': 3, 'placeholder': 'Write the answer to your question'}))

    class Meta:
        model = FAQ
        fields = ['subtitle', 'question', 'answer']

    layout = Layout('subtitle', 'question', 'answer')


class ComplaintForm(forms.ModelForm):
    title = forms.CharField(label='Title',
                            widget=forms.TextInput(attrs={'placeholder': 'e.g XYZ web application'}))
    name_of_respondent = forms.CharField(label='System Name',
                                         widget=forms.TextInput(attrs={'placeholder': 'e.g XYZ web application'}))
    address_of_respondent = forms.CharField(
        label='What storage is the system or application currently consuming?',
        widget=forms.TextInput(
            attrs={'placeholder': 'Storage with units 20Mb or 20Gb'}))
    dpo_contacted = forms.CharField(label='If YES above, what is the size of the data to be migrated?',
                                    widget=forms.TextInput(
                                        attrs={'placeholder': 'e.g. 20Mb or 20Gb'}))
    details_of_complaint = forms.CharField(label='Additional Information',
                                           help_text='Provide any other information or comments that you feel will be helpful in describing your protect needs. '
                                                     '(e.g. System Architecture, API documentation etc., Attach link to documentation if necessary)',
                                           required=False,
                                           widget=forms.Textarea(
                                               attrs={'cols': 3,
                                                      'placeholder': 'Provide any further comments'}))

    class Meta:
        model = ComplaintModel
        fields = ['title', 'name_of_respondent', 'address_of_respondent', 'dpo_contacted', 'details_of_complaint']

    layout = Layout('title', 'name_of_respondent', 'address_of_respondent', 'dpo_contacted', 'details_of_complaint')


class RepresentativeForm(forms.ModelForm):
    full_names = forms.CharField(
        label='Organization Name',
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g. National IT Authority - Uganda'}))
    title = forms.CharField(help_text='Specify the number of cores for the server',
                            widget=forms.TextInput(attrs={'placeholder': '3'}))
    address = forms.CharField(
        label='Physical Address',
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g. Mackinon Road, Plot 4, Kampala-Uganda'}))
    email_address = forms.EmailField(label='Email Address', help_text='We will communicate to you via email',
                                     widget=forms.EmailInput(attrs={'placeholder': 'example@gou.go.ug'}))
    phone_number = forms.CharField(min_length=10, max_length=15, error_messages={
        'required': 'A valid phone number is required'
    },
                                   help_text='If in another country, specify the country code e.g. +254',
                                   widget=forms.TextInput(attrs={'placeholder': '0772123456'}))
    relationship_to_complainant = forms.CharField(label='Number of Nics (Optional)',
                                                  help_text='Network Interface Cards e.g. 2',
                                                  widget=forms.NumberInput(attrs={'placeholder': 'e.g. 2'}))

    class Meta:
        model = RepresentativeModel
        fields = ['full_names', 'title', 'address', 'email_address',
                  'phone_number', 'relationship_to_complainant']

    layout = Layout('full_names', 'title',
                    Fieldset('Contact Information',
                             Row('address', 'email_address'),
                             Row('phone_number', 'relationship_to_complainant')))


class DataControllerForm(forms.ModelForm):
    full_names = forms.CharField(
        label='Organization Name',
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g. National IT Authority - Uganda'}))
    address = forms.CharField(
        label='Physical Address',
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g. Mackinon Road, Plot 4, Kampala-Uganda'}))
    email_address = forms.EmailField(label='Email Address', help_text='We will communicate to you via email',
                                     widget=forms.EmailInput(attrs={'placeholder': 'example@gou.go.ug'}))
    phone_number = forms.CharField(min_length=10, max_length=15, error_messages={
        'required': 'A valid phone number is required'
    },
                                   help_text='If in another country, specify the country code e.g. +254',
                                   widget=forms.TextInput(attrs={'placeholder': '0772123456'}))

    class Meta:
        model = DataControllerModel
        fields = ['full_names', 'address', 'email_address', 'phone_number']

    layout = Layout('full_names', 'address',
                    Row('email_address', 'phone_number'))


class DataBreachForm(forms.ModelForm):
    nature = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ubuntu 16.04 LTS'}))
    date_of_awareness = forms.CharField(help_text='Specify the number of cores for the server',
                                        widget=forms.DateInput(attrs={'placeholder': '3'}))
    subject_personal_data = forms.CharField(help_text='Specify the amount of memory with units at the end e.g. 2Gb',
                                            widget=forms.TextInput(attrs={'placeholder': '2Gb'}))
    personal_data_categories = forms.EmailField(label='Email Address', help_text='We will communicate to you via email',
                                                widget=forms.EmailInput(attrs={'placeholder': 'example@gou.go.ug'}))
    number_of_subjects = forms.CharField(help_text='Partitions should be separated by commas',
                                         widget=forms.TextInput(
                                             attrs={'placeholder': 'e.g. /home 50Gb, /swap 20Gb, /data 80Gb'}))
    details = forms.CharField(label='Number of Nics (Optional)',
                              help_text='Network Interface Cards e.g. 2',
                              widget=forms.Textarea(attrs={'placeholder': 'e.g. 2'}))
    risk_of_harm = forms.CharField(label='Number of Nics (Optional)',
                                   help_text='Network Interface Cards e.g. 2',
                                   widget=forms.Textarea(attrs={'placeholder': 'e.g. 2'}))

    class Meta:
        model = DataBreachModel
        fields = ['nature', 'date_of_awareness', 'subject_personal_data', 'personal_data_categories',
                  'number_of_subjects', 'details', 'risk_of_harm']

    layout = Layout('nature',
                    Row('date_of_awareness', 'subject_personal_data'),
                    Row('personal_data_categories', 'number_of_subjects'),
                    Fieldset('Additional Information',
                             Row('details', 'risk_of_harm')))


class RemedialMeasuresForm(forms.ModelForm):
    measures_taken = forms.CharField(label='Number of Nics (Optional)',
                                     help_text='Network Interface Cards e.g. 2',
                                     widget=forms.Textarea(attrs={'placeholder': 'e.g. 2'}))
    has_notified_regulators = forms.ChoiceField(choices=YES_NO,
                                                label='Is there any data going to be migrated from the legacy to new system?',
                                                widget=forms.Select())
    regulators_notified = forms.CharField(help_text='Partitions should be separated by commas',
                                          widget=forms.TextInput(
                                              attrs={'placeholder': 'e.g. /home 50Gb, /swap 20Gb, /data 80Gb'}))

    class Meta:
        model = DataBreachModel
        fields = ['measures_taken', 'has_notified_regulators', 'regulators_notified']

    layout = Layout('measures_taken', 'has_notified_regulators', 'regulators_notified')
