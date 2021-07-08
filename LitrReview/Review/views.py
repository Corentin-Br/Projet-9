from django.core.exceptions import ValidationError
from django.core.validators import validate_image_file_extension, get_available_image_extensions
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import CreateView, TemplateView, FormView
from django.template import loader
from django.views import View
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Review, Ticket
from .forms import RegisterForm, TicketForm, ReviewForm


class ReviewListView(generic.ListView):
    model = Review
    paginate_by = 5
    context_object_name = 'review_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    template_name = 'review/review.html'


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["user_name"]
            password = form.cleaned_data["password"]
            User.objects.create_user(username=username, password=password)
            return HttpResponseRedirect(reverse("login"))
    else:
        form = RegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'register.html', context)


class TicketCreate(CreateView):
    form_class = TicketForm
    success_url = reverse_lazy("ticket-create")
    template_name = "Review/ticket_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class ReviewCreate(CreateView):
    form_class = ReviewForm
    template_name = "Review/review_form.html"
    success_url = reverse_lazy("ticket-create")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ticket"] = get_object_or_404(Ticket, pk=self.kwargs["pk"])
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.ticket = get_object_or_404(Ticket, pk=self.kwargs["pk"])
        form.save()
        return super().form_valid(form)


class ReviewAndTicketCreate(TemplateView):
    template_name = "Review/review_form.html"
    success_url = reverse_lazy("ticket-create")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ticket_form"] = TicketForm
        context["review_form"] = ReviewForm
        return context

    def post(self, *args, **kwargs):
        content = self.request.POST
        files = self.request.FILES
        ticket_form = TicketForm({"title": content["title"],
                                  "description": content["description"]})
        review_form = ReviewForm({"headline": content["headline"],
                                  "rating": content["rating"],
                                  "body": content["body"]})
        ticket_form.instance.user = self.request.user
        ticket_form.instance.image = files["image"] if files else content["image"]
        review_form.instance.user = self.request.user
        if ticket_form.is_valid():
            ticket = ticket_form.save()
            review_form.instance.ticket = ticket
        if not ticket_form.is_valid() or not review_form.is_valid():
            try:
                Ticket.delete(Ticket.objects.get(pk=ticket.pk))
            except KeyError:
                pass
            context = {
                'ticket_form': ticket_form,
                "review_form": review_form
            }
            return render(self.request, 'Review/review_form.html', context)
        return HttpResponseRedirect(reverse_lazy("ticket-create"))

