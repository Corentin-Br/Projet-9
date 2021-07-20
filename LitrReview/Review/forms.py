from django import forms
from django.db import models
from django.forms.widgets import PasswordInput, RadioSelect
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from .models import Ticket, Review, UserFollows


class RegisterForm(forms.Form):
    user_name = forms.CharField(min_length=5,
                                max_length=32,
                                label="Nom d'utilisateur")
    # help_text="Entrez le nom qui vous servira à vous connecter, sa longueur doit être comprise entre
    # 5 et 32 caractères"
    password = forms.CharField(min_length=8,
                               label="Mot de passe",
                               widget=PasswordInput)
    # help_text="Entrez le mot de passe que vous utiliserez pour vous connecter.
    # Sa longueur doit être supérieure à 8 caractères.",
    password_check = forms.CharField(min_length=8,
                                     label="Confirmer mot de passe",
                                     widget=PasswordInput)
    #  help_text="Réentrez votre mot de passe pour le confirmer."

    def clean(self):
        data = super().clean()
        password = data.get("password")
        password_check = data.get("password_check")
        if password and password_check:
            if password != password_check:
                message = "La confirmation n'est pas identique au mot de passe! Tapez le même mot de passe pour le " \
                          "confirmer."
                self.add_error("password_check", ValidationError(message, code="Password and confirmation don't match"))
        return data

    def clean_user_name(self):
        new_user_name = self.cleaned_data["user_name"]
        try:
            User.objects.get(username=new_user_name)
        except ObjectDoesNotExist:
            return new_user_name
        else:
            raise ValidationError("Ce nom est déjà pris.", code="Username already taken")


class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        labels = {"title": "Titre"}
        # help_texts = {"title": "Entrez le titre du livre et/ou son auteur",
        #               "description": "Donnez les détails de ce que vous cherchez.",
        #               "image": "Téléversez la couverture du livre (facultatif)"}


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]
        labels = {"headline": "Titre",
                  "rating": "Note",
                  "body": "Commentaire"}
        widgets = {"rating": RadioSelect(choices=[(0, "- 0"),
                                                  (1, "- 1"),
                                                  (2, "- 2"),
                                                  (3, "- 3"),
                                                  (4, "- 4"),
                                                  (5, "- 5")],
                                         attrs={"class": "list-unstyled d-flex flex-row justify-content-around"})}


class FollowForm(forms.ModelForm):
    followed_user = forms.CharField(min_length=5,
                                    max_length=32,
                                    label="Nom d'utilisateur")

    class Meta:
        model = UserFollows
        exclude = ["user", "followed_user"]

    def clean(self):
        data = super().clean()
        username = data.get("followed_user")
        if not User.objects.filter(username=username).exists():
            self.add_error("followed_user", ValidationError("Cet utilisateur n'existe pas!",
                                                            code="User follows invalid user"))
        return data

