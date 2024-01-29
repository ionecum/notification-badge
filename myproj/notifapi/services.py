def trigger_visit_notification(person_from):
    message = _("%(username)s visited your profile") % {'username':person_from.username}
    
