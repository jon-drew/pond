import { makeServerClient } from '@/lib/urql/client';
import { RIBBITS_QUERY } from '@/gql/ribbits';
import { ME_QUERY } from '@/gql/hoppers';
import { RibbitCard } from '@/components/ribbits/ribbit-card';
import Link from 'next/link';

export default async function RibbitsPage() {
  const client = await makeServerClient();
  const [ribbitsResult, meResult] = await Promise.all([
    client.query(RIBBITS_QUERY, {}),
    client.query(ME_QUERY, {}),
  ]);

  const ribbits = ribbitsResult.data?.ribbits ?? [];
  const me = meResult.data?.me;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold text-green-400">Your Feed</h1>
        <Link
          href="/events"
          className="px-3 py-1.5 bg-green-700 hover:bg-green-600 text-black text-sm font-medium rounded-lg transition-colors"
        >
          + Ribbit
        </Link>
      </div>
      {ribbits.length === 0 && (
        <div className="text-center py-16">
          <p className="text-5xl mb-4">🐸</p>
          <p className="text-green-400 font-medium mb-1">The pond is quiet…</p>
          <p className="text-green-700 text-sm mb-4">
            Ribbits are posted at Events. Join an Event to start ribbiting!
          </p>
          <Link
            href="/events"
            className="inline-block px-4 py-2 bg-green-800 hover:bg-green-700 text-green-300 text-sm rounded-lg transition-colors"
          >
            Browse Events
          </Link>
        </div>
      )}
      {me && ribbits.map((ribbit: Parameters<typeof RibbitCard>[0]['ribbit']) => (
        <RibbitCard key={ribbit.id} ribbit={ribbit} myId={me.id} />
      ))}
    </div>
  );
}
