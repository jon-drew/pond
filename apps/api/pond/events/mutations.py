from datetime import datetime
from typing import Optional

import jwt
import strawberry
from strawberry.types import Info

from pond.events.models import Event, Ticket
from pond.events.types import EventType, TicketCheckoutType
from pond.hoppers.tokens import decode_access_token
from pond.hoppers.models import Hopper
from pond.pads.models import Pad


def _require_auth(info: Info) -> Hopper:
    from django.conf import settings
    token = info.context.request.COOKIES.get(settings.ACCESS_TOKEN_COOKIE)
    if not token:
        raise PermissionError('Authentication required')
    try:
        payload = decode_access_token(token)
    except jwt.ExpiredSignatureError:
        raise PermissionError('Token expired')
    except jwt.InvalidTokenError:
        raise PermissionError('Invalid token')
    return Hopper.objects.get(pk=payload['sub'])


@strawberry.type
class EventMutations:

    @strawberry.mutation
    def create_event(
        self,
        info: Info,
        title: str,
        text: str = '',
        start: Optional[str] = None,
        end: Optional[str] = None,
        pad_slug: Optional[str] = None,
        private: bool = True,
        ticket_price: Optional[float] = None,
    ) -> EventType:
        me = _require_auth(info)
        pad = None
        if pad_slug:
            try:
                pad = Pad.objects.get(slug=pad_slug, deleted_at__isnull=True)
            except Pad.DoesNotExist:
                raise ValueError('Pad not found')
        kwargs = {'title': title, 'text': text, 'created_by': me, 'private': private}
        if pad:
            kwargs['pad'] = pad
        if start:
            kwargs['start'] = datetime.fromisoformat(start)
        if end:
            kwargs['end'] = datetime.fromisoformat(end)
        if ticket_price is not None and ticket_price > 0:
            kwargs['ticket_price'] = ticket_price
        return Event.objects.create(**kwargs)

    @strawberry.mutation
    def update_event(
        self,
        info: Info,
        slug: str,
        title: Optional[str] = None,
        text: Optional[str] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
        private: Optional[bool] = None,
    ) -> EventType:
        me = _require_auth(info)
        try:
            event = Event.objects.get(slug=slug, deleted_at__isnull=True)
        except Event.DoesNotExist:
            raise ValueError('Event not found')
        if event.created_by != me:
            raise PermissionError('Only the creator can update this event')
        if title is not None:
            event.title = title
        if text is not None:
            event.text = text
        if start is not None:
            event.start = datetime.fromisoformat(start)
        if end is not None:
            event.end = datetime.fromisoformat(end)
        if private is not None:
            event.private = private
        event.save()
        return event

    @strawberry.mutation
    def delete_event(self, info: Info, slug: str) -> bool:
        me = _require_auth(info)
        try:
            event = Event.objects.get(slug=slug, deleted_at__isnull=True)
        except Event.DoesNotExist:
            raise ValueError('Event not found')
        if event.created_by != me:
            raise PermissionError('Only the creator can delete this event')
        event.soft_delete()
        return True

    @strawberry.mutation
    def rsvp_event(self, info: Info, slug: str) -> EventType:
        me = _require_auth(info)
        try:
            event = Event.objects.get(slug=slug, deleted_at__isnull=True)
        except Event.DoesNotExist:
            raise ValueError('Event not found')
        if me in event.attending.all():
            event.attending.remove(me)
        else:
            event.attending.add(me)
        return event

    @strawberry.mutation
    def purchase_ticket(self, info: Info, event_slug: str) -> TicketCheckoutType:
        from django.conf import settings as django_settings
        me = _require_auth(info)
        try:
            event = Event.objects.get(slug=event_slug, deleted_at__isnull=True)
        except Event.DoesNotExist:
            raise ValueError('Event not found')
        if not event.ticket_price:
            raise ValueError('This event is free — no ticket required')
        ticket, _ = Ticket.objects.get_or_create(event=event, hopper=me)
        if ticket.status == Ticket.STATUS_PAID:
            raise ValueError('You already have a ticket for this event')

        stripe_key = getattr(django_settings, 'STRIPE_SECRET_KEY', None)
        if not stripe_key:
            raise ValueError('Ticketing is not configured on this server')

        import stripe
        stripe.api_key = stripe_key
        origin = info.context.request.headers.get('Origin', 'https://pond.app')
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(event.ticket_price * 100),
                    'product_data': {'name': f'Ticket: {event.title}'},
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f'{origin}/events/{event.slug}?ticket=success',
            cancel_url=f'{origin}/events/{event.slug}?ticket=cancel',
            metadata={'ticket_id': str(ticket.pk)},
        )
        ticket.stripe_session_id = session.id
        ticket.save(update_fields=['stripe_session_id'])
        return TicketCheckoutType(checkout_url=session.url, ticket_id=ticket.pk)

    @strawberry.mutation
    def confirm_ticket(self, info: Info, session_id: str) -> bool:
        try:
            ticket = Ticket.objects.get(stripe_session_id=session_id)
        except Ticket.DoesNotExist:
            raise ValueError('Ticket not found')
        from django.conf import settings as django_settings
        import stripe
        stripe.api_key = getattr(django_settings, 'STRIPE_SECRET_KEY', '')
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status == 'paid':
            ticket.status = Ticket.STATUS_PAID
            ticket.amount_paid = ticket.event.ticket_price
            ticket.save(update_fields=['status', 'amount_paid'])
            ticket.event.attending.add(ticket.hopper)
            return True
        return False
