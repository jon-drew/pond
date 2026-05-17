import { makeServerClient } from '@/lib/urql/client';
import { PAD_QUERY } from '@/gql/pads';
import { EVENTS_QUERY } from '@/gql/events';
import Link from 'next/link';

export default async function PadDetailPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const client = await makeServerClient();
  const result = await client.query(PAD_QUERY, { slug });
  const pad = result.data?.pad;

  if (!pad) return <p className="text-green-700">Pad not found.</p>;

  return (
    <div className="space-y-6">
      <div className="bg-black rounded-2xl border border-green-800 p-6">
        <div className="flex items-start gap-4">
          <span className="text-4xl">🌿</span>
          <div>
            <h1 className="text-xl font-bold text-green-400">{pad.name}</h1>
            <p className="text-green-700 text-sm">{pad.address}</p>
            {pad.description && <p className="mt-2 text-sm">{pad.description}</p>}
            {pad.owner && <p className="mt-1 text-xs text-green-700">Owned by <a href={`/hoppers/${pad.owner.slug}`} className="text-green-400 hover:text-green-300">{pad.owner.username}</a></p>}
          </div>
        </div>
      </div>
      <div className="flex items-center justify-between">
        <h2 className="font-semibold text-green-400">Events at this Pad</h2>
        <Link href={`/events/new?pad=${pad.slug}`} className="text-sm text-green-400 hover:text-green-300">+ New Event here</Link>
      </div>
    </div>
  );
}
