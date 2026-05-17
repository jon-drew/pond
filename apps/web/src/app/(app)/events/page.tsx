import { makeServerClient } from '@/lib/urql/client';
import { EVENTS_QUERY } from '@/gql/events';
import Link from 'next/link';
import { format } from 'date-fns';

export default async function EventsPage() {
  const client = await makeServerClient();
  const result = await client.query(EVENTS_QUERY, {});
  const events = result.data?.events ?? [];

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold text-green-400">Events</h1>
        <Link href="/events/new"
          className="px-3 py-1.5 bg-green-700 hover:bg-green-600 text-black text-sm rounded-lg transition-colors"
        >
          + New Event
        </Link>
      </div>
      <div className="grid gap-3">
        {events.map((e: { id: string; title: string; text: string; slug: string; start: string; pad: { name: string } | null; private: boolean }) => (
          <Link key={e.id} href={`/events/${e.slug}`}
            className="bg-black rounded-xl border border-green-800 p-4 hover:border-green-600 transition-colors"
          >
            <div className="flex items-start justify-between">
              <div>
                <p className="font-medium">{e.title}</p>
                {e.pad && <p className="text-xs text-green-700">🌿 {e.pad.name}</p>}
                {e.text && <p className="text-sm text-green-700 mt-1 line-clamp-2">{e.text}</p>}
              </div>
              <div className="text-right text-xs text-green-700 shrink-0 ml-4">
                <p>{format(new Date(e.start), 'MMM d, h:mm a')}</p>
                {e.private && <span className="text-yellow-500">Private</span>}
              </div>
            </div>
          </Link>
        ))}
        {events.length === 0 && <p className="text-green-700 text-sm">No events yet.</p>}
      </div>
    </div>
  );
}
