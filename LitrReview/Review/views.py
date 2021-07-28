from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db.models import CharField, Value, Q
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView

from itertools import chain

from .models import Review, Ticket, UserFollows
from .forms import RegisterForm, TicketForm, ReviewForm, FollowForm


class FeedView(LoginRequiredMixin, generic.ListView):
    paginate_by = 5
    context_object_name = 'feed'

    def get_queryset(self, **kwargs):
        follows = [follow.followed_user for follow in UserFollows.objects.filter(user=self.request.user)]

        reviews = Review.objects.filter(Q(user=self.request.user) | Q(user__in=follows) | Q(ticket__user=self.request.user))
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
        tickets = Ticket.objects.filter(Q(user=self.request.user) | Q(user__in=follows))
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

        posts = sorted(
            chain(reviews, tickets),
            key=lambda post: post.time_created,
            reverse=True)
        return posts

    template_name = 'review/full_feed.html'


class SelfFeedView(LoginRequiredMixin, generic.ListView):
    paginate_by = 5
    context_object_name = 'feed'

    def get_queryset(self, **kwargs):
        reviews = Review.objects.filter(user=self.request.user)
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
        tickets = Ticket.objects.filter(user=self.request.user)
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

        posts = sorted(
            chain(reviews, tickets),
            key=lambda post: post.time_created,
            reverse=True)
        return posts

    template_name = 'review/self_feed.html'


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


class TicketCreate(LoginRequiredMixin, CreateView):
    form_class = TicketForm
    template_name = "Review/ticket_creation.html"
    success_url = reverse_lazy("feed")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class ReviewCreate(LoginRequiredMixin, CreateView):
    form_class = ReviewForm
    template_name = "Review/review_creation.html"
    success_url = reverse_lazy("feed")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ticket"] = get_object_or_404(Ticket, pk=self.kwargs["pk"])
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.ticket = get_object_or_404(Ticket, pk=self.kwargs["pk"])
        form.save()
        return super().form_valid(form)


class ReviewUpdate(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "Review/review_edit.html"
    success_url = reverse_lazy("feed")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == request.user:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponse("Vous ne pouvez pas modifier une critique que vous n'avez pas créée.", status=401)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ticket"] = get_object_or_404(Ticket, pk=self.kwargs["pk"])
        return context


class TicketUpdate(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = "Review/ticket_edit_form.html"
    success_url = reverse_lazy("feed")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == request.user:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponse("Vous ne pouvez pas modifier un ticket que vous n'avez pas créé.", status=401)


class ReviewDelete(LoginRequiredMixin, DeleteView):
    model = Review
    success_url = reverse_lazy("feed")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == request.user:
            return super().post(self, request, *args, **kwargs)
        else:
            return HttpResponse("Vous ne pouvez pas supprimer une critique que vous n'avez pas créée.", status=401)


class TicketDelete(LoginRequiredMixin, DeleteView):
    model = Ticket
    success_url = reverse_lazy("feed")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == request.user:
            return super().post(self, request, *args, **kwargs)
        else:
            return HttpResponse("Vous ne pouvez pas supprimer un ticket que vous n'avez pas créé.", status=401)


class ReviewAndTicketCreate(LoginRequiredMixin, TemplateView):
    template_name = "Review/review_creation.html"
    success_url = reverse_lazy("feed")

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
            Ticket.objects.filter(pk=ticket.pk).delete()
            context = {
                'ticket_form': ticket_form,
                "review_form": review_form
            }
            return render(self.request, 'Review/review_form.html', context)
        review_form.save()
        return HttpResponseRedirect(reverse_lazy("feed"))


class FollowView(LoginRequiredMixin, TemplateView):
    template_name = "Review/follow.html"
    success_url = reverse_lazy("follows")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        followed = [follow.followed_user for follow in UserFollows.objects.filter(user=self.request.user)]
        follower = [follow.user for follow in UserFollows.objects.filter(followed_user=self.request.user)]
        context["user_followed"] = followed
        context["user_followers"] = follower
        context["form"] = FollowForm
        return context

    def post(self, *args, **kwargs):
        content = self.request.POST
        if "follow_to_remove" in content:
            UserFollows.objects.filter(user=self.request.user,
                                       followed_user__username=content["follow_to_remove"]).delete()
            context = self.get_context_data()
            context["has_deleted"] = True
            return render(self.request, 'Review/follow.html', context)
        else:
            form = FollowForm({"followed_user": content["followed_user"]})
            form.instance.user = self.request.user
            form.instance.followed_user = User.objects.get(username=content["followed_user"])
            if form.is_valid():
                if form.instance.user == User.objects.get(username=content["followed_user"]):
                    form.add_error("followed_user", ValidationError("Vous ne pouvez pas vous suivre vous-même!",
                                                               code="User follows themselves"))
                elif UserFollows.objects.filter(user=self.request.user,
                                                followed_user__username=content["followed_user"]).exists():
                    form.add_error("followed_user", ValidationError("Vous suivez déjà cette personne!",
                                                               code="User follows already"))
                else:
                    form.save()
                    return HttpResponseRedirect(reverse_lazy("follows"))
            context = self.get_context_data()
            context["form"] = form
            return render(self.request, 'Review/follow.html', context)

