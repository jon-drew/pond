'use client';

import React, { useState, useEffect } from 'react';
import { useQuery, useMutation } from 'urql';
import { HOPPER_QUERY, ME_QUERY, FOLLOW_HOPPER_MUTATION, HOPPER_EVENTS_QUERY } from '@/gql/hoppers';
import { format } from 'date-fns';

export default function HopperDetailPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = React.use(params);
  const [hopperResult] = useQuery({ query: HOPPER_QUERY, variables: { slug } });
  const [meResult] = useQuery({ query: ME_QUERY });
  const [eventsResult] = useQuery({ query: HOPPER_EVENTS_QUERY, variables: { slug } });
  const [, follow] = useMutation(FOLLOW_HOPPER_MUTATION);

  const hopper = hopperResult.data?.hopper;
  const me = meResult.data?.me;
  const events: Array<{ id: string; title: string; text: string; start: string; slug: string; private: boolean; pad: { name: string; slug: string } | null }> =
    eventsResult.data?.hopperEvents ?? [];

  const [following, setFollowing] = useState<boolean | null>(null);

  useEffect(() => {
    if (hopper?.isFollowedByMe !== undefined) {
      setFollowing(hopper.isFollowedByMe);
    }
  }, [hopper?.isFollowedByMe]);

  if (hopperResult.fetching) return <p className="text-green-700">Loading…</p>;
  if (!hopper) return <p className="text-green-700">Hopper not found.</p>;

  const isMe = me?.id === hopper.id;

  async function handleFollowToggle() {
    const next = !following;
    setFollowing(next);
    await follow({ slug: hopper.slug });
  }

  return (
    <div className="space-y-4">
      <div className="bg-black rounded-2xl border border-green-800 p-6 flex items-start justify-between">
        <div className="flex items-center gap-4">
          <span className="text-5xl">🐸</span>
          <div>
            <h1 className="text-xl font-bold text-green-400">{hopper.name || hopper.username}</h1>
            <p className="text-green-700 text-sm">@{hopper.username}</p>
          </div>
        </div>
        {!isMe && me && (
          <button
            onClick={handleFollowToggle}
            className={`px-4 py-2 text-sm rounded-lg transition-colors ${
              following
                ? 'bg-green-900 border border-green-600 text-green-300 hover:bg-red-900 hover:border-red-600 hover:text-red-300'
                : 'bg-green-700 hover:bg-green-600 text-black'
            }`}
          >
            {following ? 'Hopping ✓' : 'Hop to'}
          </button>
        )}
      </div>

      <div className="space-y-3">
        <h2 className="font-semibold text-green-400">Events Ribbited</h2>
        {eventsResult.fetching && <p className="text-green-700 text-sm">Loading…</p>}
        {events.map((e) => (
          <a key={e.id} href={`/events/${e.slug}`}
            className="block bg-black rounded-xl border border-green-800 p-4 hover:border-green-600 transition-colors"
          >
            <div className="flex items-start justify-between">
              <div>
                <p className="font-medium">{e.title}</p>
                {e.pad && <p className="text-xs text-green-700 mt-0.5">🌿 {e.pad.name}</p>}
                {e.text && <p className="text-sm text-green-700 mt-1 line-clamp-2">{e.text}</p>}
              </div>
              <div className="text-right text-xs text-green-700 shrink-0 ml-4">
                <p>{format(new Date(e.start), 'MMM d, h:mm a')}</p>
                {e.private && <span className="text-yellow-500">Private</span>}
              </div>
            </div>
          </a>
        ))}
        {!eventsResult.fetching && events.length === 0 && (
          <div className="text-center py-8">
            <p className="text-3xl mb-2">🐸</p>
            <p className="text-green-700 text-sm">No events ribbited yet.</p>
          </div>
        )}
      </div>
    </div>
  );
}
