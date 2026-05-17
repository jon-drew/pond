import { makeServerClient } from '@/lib/urql/client';
import { RIBBITS_QUERY } from '@/gql/ribbits';
import { ME_QUERY } from '@/gql/hoppers';
import { RibbitCard } from '@/components/ribbits/ribbit-card';

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
      <h1 className="text-xl font-bold text-green-400">Your Feed</h1>
      {ribbits.length === 0 && (
        <p className="text-green-700 text-sm">
          No Ribbits yet. Follow some Hoppers or attend some Events to see their Ribbits here.
        </p>
      )}
      {me && ribbits.map((ribbit: Parameters<typeof RibbitCard>[0]['ribbit']) => (
        <RibbitCard key={ribbit.id} ribbit={ribbit} myId={me.id} />
      ))}
    </div>
  );
}
