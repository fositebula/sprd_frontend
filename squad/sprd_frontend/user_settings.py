import logging

from django import forms
from django.conf.urls import url
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


from rest_framework.authtoken.models import Token


from squad.core.models import Group, Subscription


logger = logging.getLogger()


@login_required
def home(request):
    return redirect(reverse('settings-profile'))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(request.path)
        else:
            context = {'form': form}
    else:
        context = {'form': ProfileForm(instance=request.user)}
    return render(request, 'squad/user_settings/profile.jinja2', context)


@login_required
def api_token(request):
    try:
        token = Token.objects.get(user=request.user)
    except Token.DoesNotExist:
        token = None

    if request.method == "POST":
        if token:
            token.delete()
        token = Token.objects.create(user=request.user)
        return redirect(reverse('settings-api-token'))

    context = {'token': token}
    return render(request, 'squad/user_settings/api_token.jinja2', context)


@login_required
def subscriptions(request):

    subscriptions = Subscription.objects.filter(user=request.user)
    groups = Group.objects.all().prefetch_related('projects')

    if request.method == "POST":
        try:
            Subscription.objects.create(
                project_id=request.POST.get("subscription"),
                notification_strategy=request.POST.get(
                    "notification-strategy"),
                user=request.user
            )
        except IntegrityError:
            logger.warning("Subscription for given user %s already exists on project: %s", request.user, request.POST.get("subscription"))
            pass

        return redirect(reverse('settings-subscriptions'))

    context = {
        'subscriptions': subscriptions,
        'groups': groups,
        'notification_strategies': {elem[0]: elem[1] for elem in
                                    Subscription.STRATEGY_CHOICES},
    }
    return render(request, 'squad/user_settings/subscriptions.jinja2', context)


@login_required
def remove_subscription(request, id):

    subscription = get_object_or_404(Subscription, pk=id, user=request.user)
    subscription.delete()
    return redirect(reverse('settings-subscriptions'))


urls = [
    url('^$', home, name='settings-home'),
    url('^profile/$', profile, name='settings-profile'),
    url('^api-token/$', api_token, name='settings-api-token'),
    url('^subscriptions/$', subscriptions, name='settings-subscriptions'),
    url(r'^remove-subscription/(?P<id>\d+)$', remove_subscription, name='settings-subscription-remove'),
]
