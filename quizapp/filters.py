from django_filters import FilterSet, CharFilter
from django import forms
from .models import Result


class ResultFilter(FilterSet):
    total = CharFilter(lookup_expr='icontains', label='Total',
                       widget=forms.TextInput(attrs={'class': 'form-control'})
                       )
    first_name = CharFilter(field_name='views', lookup_expr='gt', label='First Name',
                        widget=forms.TextInput(attrs={'class': 'form-control'})
                        )
    last_name = CharFilter(field_name='views', lookup_expr='lt', label='Last Name',
                        widget=forms.TextInput(attrs={'class': 'form-control'})
                        )

    class Meta:
        model = Result
        fields = ['total', 'first_name', 'last_name']