def unread_notifications(request):
    """
    Makes the count of unread notifications globally available
    to all templates for the authenticated user.
    """
    if request.user.is_authenticated:
        count = request.user.notifications.filter(is_read=False).count()
        return {"unread_notifications_count": count}
    return {}
