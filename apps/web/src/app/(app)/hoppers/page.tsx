import { makeServerClient } from '@/lib/urql/client';
import { HOPPERS_QUERY } from '@/gql/hoppers';
import Link from 'next/link';

export default async function HoppersPage() {
  const client = await makeServerClient();
  const result = await client.query(HOPPERS_QUERY, {});
  const hoppers = result.data?.hoppers ?? [];

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-bold">Hoppers</h1>
      <div className="grid gap-3">
        {hoppers.map((h: { id: string; username: string; name: string; slug: string }) => (
          <Link key={h.id} href={`/hoppers/${h.slug}`}
            className="bg-white rounded-xl border border-gray-200 p-4 flex items-center gap-3 hover:border-pond-400 transition-colors"
          >
            <span className="text-2xl">🐸</span>
            <div>
              <p className="font-medium">{h.name || h.username}</p>
              <p className="text-xs text-gray-500">@{h.username}</p>
            </div>
          </Link>
        ))}
        {hoppers.length === 0 && <p className="text-gray-500 text-sm">No public Hoppers yet.</p>}
      </div>
    </div>
  );
}
