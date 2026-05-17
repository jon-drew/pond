import { makeServerClient } from '@/lib/urql/client';
import { HOPPERS_QUERY } from '@/gql/hoppers';
import Link from 'next/link';

export default async function HoppersPage() {
  const client = await makeServerClient();
  const result = await client.query(HOPPERS_QUERY, {});
  const hoppers = result.data?.hoppers ?? [];

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-bold text-green-400">Hoppers</h1>
      <div className="grid gap-3">
        {hoppers.map((h: { id: string; username: string; name: string; slug: string }) => (
          <Link key={h.id} href={`/hoppers/${h.slug}`}
            className="bg-black rounded-xl border border-green-800 p-4 flex items-center gap-3 hover:border-green-600 transition-colors"
          >
            <span className="text-2xl">🐸</span>
            <div>
              <p className="font-medium">{h.name || h.username}</p>
              <p className="text-xs text-green-700">@{h.username}</p>
            </div>
          </Link>
        ))}
        {hoppers.length === 0 && <p className="text-green-700 text-sm">No public Hoppers yet.</p>}
      </div>
    </div>
  );
}
