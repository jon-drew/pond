'use client';

import { useQuery, useMutation } from 'urql';
import { HOPPER_QUERY, ME_QUERY, FOLLOW_HOPPER_MUTATION } from '@/gql/hoppers';
import { cn } from '@/lib/utils';

export default function HopperDetailPage({ params }: { params: { slug: string } }) {
  const [hopperResult] = useQuery({ query: HOPPER_QUERY, variables: { slug: params.slug } });
  const [meResult] = useQuery({ query: ME_QUERY });
  const [, follow] = useMutation(FOLLOW_HOPPER_MUTATION);

  const hopper = hopperResult.data?.hopper;
  const me = meResult.data?.me;

  if (hopperResult.fetching) return <p className="text-gray-400">Loading…</p>;
  if (!hopper) return <p className="text-gray-500">Hopper not found.</p>;

  const isMe = me?.id === hopper.id;

  return (
    <div className="space-y-4">
      <div className="bg-white rounded-2xl border border-gray-200 p-6 flex items-start justify-between">
        <div className="flex items-center gap-4">
          <span className="text-5xl">🐸</span>
          <div>
            <h1 className="text-xl font-bold">{hopper.name || hopper.username}</h1>
            <p className="text-gray-500 text-sm">@{hopper.username}</p>
          </div>
        </div>
        {!isMe && me && (
          <button
            onClick={() => follow({ slug: hopper.slug })}
            className="px-4 py-2 bg-pond-600 hover:bg-pond-700 text-white text-sm rounded-lg transition-colors"
          >
            Follow / Unfollow
          </button>
        )}
      </div>
    </div>
  );
}
