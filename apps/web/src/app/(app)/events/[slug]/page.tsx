'use client';

import React from 'react';
import { useQuery, useMutation } from 'urql';
import { EVENT_QUERY } from '@/gql/events';
import { ME_QUERY } from '@/gql/hoppers';
import { RSVP_EVENT_MUTATION } from '@/gql/events';
import { CREATE_RIBBIT_MUTATION } from '@/gql/ribbits';
import { RIBBITS_QUERY } from '@/gql/ribbits';
import { RibbitCard } from '@/components/ribbits/ribbit-card';
import { format } from 'date-fns';
import Link from 'next/link';
import { cn } from '@/lib/utils';

export default function EventDetailPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = React.use(params);
  const [eventResult, refetchEvent] = useQuery({ query: EVENT_QUERY, variables: { slug } });
  const [meResult] = useQuery({ query: ME_QUERY });
  const [ribbitsResult, refetchRibbits] = useQuery({ query: RIBBITS_QUERY });
  const [, rsvp] = useMutation(RSVP_EVENT_MUTATION);
  const [, createRibbit] = useMutation(CREATE_RIBBIT_MUTATION);

  const event = eventResult.data?.event;
  const me = meResult.data?.me;
  const allRibbits = ribbitsResult.data?.ribbits ?? [];
  const eventRibbits = allRibbits.filter((r: { event: { slug: string } }) => r.event.slug === slug);

  if (eventResult.fetching) return <p className="text-green-700">Loading…</p>;
  if (!event) return <p className="text-green-700">Event not found.</p>;

  const isOwner = me?.id === event.createdBy?.id;
  const isAttending = event.attending.some((h: { id: string }) => h.id === me?.id);
  const hasRibbited = allRibbits.some(
    (r: { sentBy: { id: string }; event: { slug: string } }) =>
      r.sentBy.id === me?.id && r.event.slug === slug
  );

  const [rsvpPending, setRsvpPending] = React.useState(false);
  const [ribbitPending, setRibbitPending] = React.useState(false);
  const [bothPending, setBothPending] = React.useState(false);

  async function handleAttend() {
    setRsvpPending(true);
    await rsvp({ slug: event.slug });
    refetchEvent({ requestPolicy: 'network-only' });
    setRsvpPending(false);
  }

  async function handleRibbit() {
    if (hasRibbited) return;
    setRibbitPending(true);
    await createRibbit({ eventSlug: event.slug });
    refetchRibbits({ requestPolicy: 'network-only' });
    setRibbitPending(false);
  }

  async function handleAttendAndRibbit() {
    setBothPending(true);
    if (!isAttending) await rsvp({ slug: event.slug });
    if (!hasRibbited) await createRibbit({ eventSlug: event.slug });
    refetchEvent({ requestPolicy: 'network-only' });
    refetchRibbits({ requestPolicy: 'network-only' });
    setBothPending(false);
  }

  return (
    <div className="space-y-6">
      <div className="bg-black rounded-2xl border border-green-800 p-6 space-y-3">
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-xl font-bold text-green-400">{event.title}</h1>
            {event.pad && <p className="text-sm text-green-700">🌿 <a href={`/pads/${event.pad.slug}`} className="hover:text-green-400">{event.pad.name}</a></p>}
          </div>
          {event.private && <span className="text-xs bg-yellow-950 text-yellow-400 border border-yellow-800 px-2 py-0.5 rounded">Private</span>}
        </div>
        {event.text && <p className="text-sm text-green-300">{event.text}</p>}
        <div className="text-xs text-green-700">
          <p>Starts: {format(new Date(event.start), 'MMM d, yyyy h:mm a')}</p>
          <p>Ends: {format(new Date(event.end), 'MMM d, yyyy h:mm a')}</p>
          <p>{event.attending.length} attending</p>
        </div>
        <div className="flex flex-wrap gap-2">
          <button
            onClick={handleAttend}
            disabled={rsvpPending || bothPending}
            className={cn(
              'px-4 py-2 text-sm rounded-lg border transition-colors disabled:opacity-50',
              isAttending
                ? 'bg-green-950 border-green-700 text-green-400 hover:bg-green-900'
                : 'bg-black border-green-800 text-green-700 hover:border-green-600 hover:text-green-400'
            )}
          >
            {rsvpPending ? '…' : isAttending ? '✓ Attending' : 'Attend'}
          </button>
          <button
            onClick={handleRibbit}
            disabled={hasRibbited || ribbitPending || bothPending}
            className={cn(
              'px-4 py-2 text-sm rounded-lg border transition-colors disabled:opacity-50',
              hasRibbited
                ? 'bg-green-950 border-green-700 text-green-400 cursor-default'
                : 'bg-black border-green-800 text-green-700 hover:border-green-600 hover:text-green-400'
            )}
          >
            {ribbitPending ? '…' : hasRibbited ? '🐸 Ribbited' : '🐸 Ribbit'}
          </button>
          <button
            onClick={handleAttendAndRibbit}
            disabled={bothPending || rsvpPending || ribbitPending || (isAttending && hasRibbited)}
            className={cn(
              'px-4 py-2 text-sm rounded-lg border transition-colors disabled:opacity-50',
              isAttending && hasRibbited
                ? 'bg-green-950 border-green-700 text-green-400 cursor-default'
                : 'bg-green-700 border-green-600 text-black hover:bg-green-600'
            )}
          >
            {bothPending ? '…' : isAttending && hasRibbited ? '✓ Done' : 'Attend + Ribbit'}
          </button>
          {isOwner && (
            <Link href={`/events/${slug}/patterns`}
              className="px-4 py-2 text-sm bg-blue-950 hover:bg-blue-900 text-blue-400 rounded-lg border border-blue-900 transition-colors"
            >
              📊 View Patterns
            </Link>
          )}
        </div>
      </div>
      <div className="space-y-3">
        <h2 className="font-semibold text-green-400">Ribbits</h2>
        {me && eventRibbits.map((r: Parameters<typeof RibbitCard>[0]['ribbit']) => (
          <RibbitCard key={r.id} ribbit={r} myId={me.id} />
        ))}
        {eventRibbits.length === 0 && <p className="text-green-700 text-sm">No Ribbits yet. Click Ribbit to add yours to the feed!</p>}
      </div>
    </div>
  );
}
