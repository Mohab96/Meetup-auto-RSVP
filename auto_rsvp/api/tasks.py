from meetup.api import Client
from celery import shared_task
from auto_rsvp.api.models import Group, User


@shared_task
def check_for_new_events():
    for user in User.objects.all():
        api_key = user.meetup_api_key

        if api_key:
            client = Client(api_key)
            for group in Group.objects.filter(user=user):
                events = client.GetEvents(
                    {'group_id': group.group_id, 'status': 'upcoming', 'rsvp': 'none'})
                for event in events:
                    rsvp_to_event.delay(user, event)


@shared_task
def rsvp_to_event(user, event):
    client = Client(user.meetup_api_key)
    try:
        event_id = event.event_id
        client.RSVP('yes', {'event_id': event_id})
    except Exception as e:
        print(f"Error RSVPing to event: {e}")
