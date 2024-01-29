from django.shortcuts import render
from notifapi.models import NotifyModel as Notifier
from django.contrib.auth.models import User

def trigger_visit_notification(request, visitor):
    message = ("%(username)s visited your profile") % {'username':visitor.username}
    Notifier.objects.addNotification(5, request.user, visitor, '',message)
    
def load_profile(request, username):
    user = User.objects.get(username=username)
    template_name = 'profiles/personal_profile.html'
    trigger_visit_notification(request,user)
    context = {
        'user': user,
    }
    return render(request, template_name, context)

