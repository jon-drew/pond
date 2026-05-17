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

export default function EventDetailPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = React.use(params);
  const [eventResult, refetchEvent] = useQuery({ query: EVENT_QUERY, variables: { slug } });
  const [meResult] = useQuery({ query: ME_QUERY });
  const [ribbitsResult] = useQuery({ query: RIBBITS_QUERY });
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

  async function handleRsvp() {
    await rsvp({ slug: event.slug });
    if (!isAttending) await createRibbit({ eventSlug: event.slug });
    refetchEvent({ requestPolicy: 'network-only' });
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
        <div className="flex gap-3">
          <button
            onClick={handleRsvp}
            className={`px-4 py-2 text-sm rounded-lg transition-colors ${isAttending ? 'bg-green-950 hover:bg-green-900 text-green-400' : 'bg-green-700 hover:bg-green-600 text-black'}`}
          >
            {isAttending ? '✓ Attending (cancel)' : 'RSVP / Ribbit'}
          </button>
          {isOwner && (
            <Link href={`/events/${slug}/patterns`}
              className="px-4 py-2 text-sm bg-blue-950 hover:bg-blue-900 text-blue-400 rounded-lg transition-colors"
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
        {eventRibbits.length === 0 && <p className="text-green-700 text-sm">No Ribbits yet. RSVP to add yours!</p>}
      </div>
    </div>
  );
}
