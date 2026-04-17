from django import template

register = template.Library()


@register.filter
def reaction_count(message, reaction_type):
    return message.reactions.filter(reaction_type=reaction_type).count()


@register.filter
def unread_notifications_count(profile):
    return profile.notifications.filter(is_read=False).count()
