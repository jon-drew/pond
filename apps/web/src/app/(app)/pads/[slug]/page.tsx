import { makeServerClient } from '@/lib/urql/client';
import { PAD_QUERY } from '@/gql/pads';
import { EVENTS_QUERY } from '@/gql/events';
import Link from 'next/link';

export default async function PadDetailPage({ params }: { params: { slug: string } }) {
  const client = await makeServerClient();
  const result = await client.query(PAD_QUERY, { slug: params.slug });
  const pad = result.data?.pad;

  if (!pad) return <p className="text-gray-500">Pad not found.</p>;

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-2xl border border-gray-200 p-6">
        <div className="flex items-start gap-4">
          <span className="text-4xl">🌿</span>
          <div>
            <h1 className="text-xl font-bold">{pad.name}</h1>
            <p className="text-gray-500 text-sm">{pad.address}</p>
            {pad.description && <p className="mt-2 text-sm">{pad.description}</p>}
            {pad.owner && <p className="mt-1 text-xs text-gray-400">Owned by <a href={`/hoppers/${pad.owner.slug}`} className="hover:underline">{pad.owner.username}</a></p>}
          </div>
        </div>
      </div>
      <div className="flex items-center justify-between">
        <h2 className="font-semibold">Events at this Pad</h2>
        <Link href={`/events/new?pad=${pad.slug}`} className="text-sm text-pond-600 hover:underline">+ New Event here</Link>
      </div>
    </div>
  );
}
