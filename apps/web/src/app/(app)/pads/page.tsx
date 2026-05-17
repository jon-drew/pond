import { makeServerClient } from '@/lib/urql/client';
import { PADS_QUERY } from '@/gql/pads';
import Link from 'next/link';

export default async function PadsPage() {
  const client = await makeServerClient();
  const result = await client.query(PADS_QUERY, {});
  const pads = result.data?.pads ?? [];

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold text-green-400">Pads</h1>
        <Link href="/pads/new"
          className="px-3 py-1.5 bg-green-700 hover:bg-green-600 text-black text-sm rounded-lg transition-colors"
        >
          + New Pad
        </Link>
      </div>
      <div className="grid gap-3">
        {pads.map((p: { id: string; name: string; address: string; slug: string }) => (
          <Link key={p.id} href={`/pads/${p.slug}`}
            className="bg-black rounded-xl border border-green-800 p-4 flex items-start gap-3 hover:border-green-600 transition-colors"
          >
            <span className="text-2xl">🌿</span>
            <div>
              <p className="font-medium">{p.name}</p>
              <p className="text-xs text-green-700">{p.address}</p>
            </div>
          </Link>
        ))}
        {pads.length === 0 && <p className="text-green-700 text-sm">No Pads yet.</p>}
      </div>
    </div>
  );
}
