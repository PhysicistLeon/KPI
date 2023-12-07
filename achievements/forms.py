from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Researcher, Article
from django.db import transaction
from django.utils.translation import gettext_lazy as _


class ResearcherForm(forms.ModelForm):
    class Meta:
        model = Researcher
        fields = ["department", "position"]


class CustomUserCreationForm(UserCreationForm):
    department = forms.CharField(required=True)
    position = forms.CharField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "department",
            "position",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        with transaction.atomic():
            user = super().save(commit=False)
            if commit:
                user.save()
                Researcher.objects.create(
                    user=user,
                    department=self.cleaned_data["department"],
                    position=self.cleaned_data["position"],
                )
        return user

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     if commit:
    #         user.save()
    #         Researcher.objects.create(
    #             user=user,
    #             department=self.cleaned_data["department"],
    #             position=self.cleaned_data["position"],
    #         )
    #     return user

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     if commit:
    #         user.save()
    #         Researcher.objects.create(
    #             user=user,
    #             department=self.cleaned_data["department"],
    #             position=self.cleaned_data["position"],
    #         )
    #     return user


from .utils import get_article_data_from_doi


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            "doi",
            "title",
            "journal_name",
            "impact_factor",
            "number_of_co_authors",
            "number_of_co_authors_from_organization",
            "researchers",
            "link_to_resource",
            "file_upload",
        ]
        labels = {
            "doi": _("DOI"),
            "title": _("Название"),
            "journal_name": _("Название журнала"),
            "impact_factor": _("Импакт-фактор"),
            "number_of_co_authors": _("Число авторов"),
            "number_of_co_authors_from_organization": _("Число авторов из НТЦ"),
            "researchers": _("Соавторы из НТЦ"),
            "link_to_resource": _("Онлайн-ресурс"),
            "file_upload": _("Загрузка файла"),
        }
        # Add any other fields you want to include in the form

    # def clean_doi(self):
    #     doi = self.cleaned_data.get("doi")
    #     if doi:
    #         article_data = get_article_data_from_doi(doi)
    #         if article_data:
    #             for field, value in article_data.items():
    #                 self.fields[field].initial = value
    #         else:
    #             raise forms.ValidationError("Invalid DOI or no data found.")
    #     return doi
