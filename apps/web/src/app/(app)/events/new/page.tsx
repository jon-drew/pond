'use client';

import { useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useMutation, useQuery } from 'urql';
import { CREATE_EVENT_MUTATION } from '@/gql/events';
import { PADS_QUERY } from '@/gql/pads';
import { cn } from '@/lib/utils';

export default function NewEventPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const defaultPad = searchParams.get('pad') ?? '';
  const [, createEvent] = useMutation(CREATE_EVENT_MUTATION);
  const [padsResult] = useQuery({ query: PADS_QUERY });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    const fd = new FormData(e.currentTarget);
    const result = await createEvent({
      title: fd.get('title') as string,
      text: fd.get('text') as string,
      start: fd.get('start') as string || null,
      end: fd.get('end') as string || null,
      padSlug: fd.get('padSlug') as string || null,
      private: fd.get('private') === 'on',
    });
    setLoading(false);
    if (result.error) { setError(result.error.graphQLErrors[0]?.message ?? result.error.message); return; }
    router.push(`/events/${result.data.createEvent.slug}`);
  }

  const pads = padsResult.data?.pads ?? [];

  return (
    <div className="max-w-md space-y-6">
      <h1 className="text-xl font-bold text-green-400">New Event</h1>
      <form onSubmit={handleSubmit} className="bg-black rounded-2xl border border-green-800 p-6 space-y-4">
        {error && <p className="text-sm text-red-400 bg-red-950 border border-red-800 rounded px-3 py-2">{error}</p>}
        <div>
          <label className="block text-sm font-medium mb-1 text-green-400">Title</label>
          <input name="title" required className="w-full bg-black border border-green-800 rounded-lg px-3 py-2 text-sm text-green-300 placeholder-green-900 focus:outline-none focus:ring-2 focus:ring-green-600" />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1 text-green-400">Description</label>
          <textarea name="text" rows={3} className="w-full bg-black border border-green-800 rounded-lg px-3 py-2 text-sm text-green-300 placeholder-green-900 focus:outline-none focus:ring-2 focus:ring-green-600" />
        </div>
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-sm font-medium mb-1 text-green-400">Start</label>
            <input name="start" type="datetime-local" className="w-full bg-black border border-green-800 rounded-lg px-3 py-2 text-sm text-green-300 focus:outline-none focus:ring-2 focus:ring-green-600" />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1 text-green-400">End</label>
            <input name="end" type="datetime-local" className="w-full bg-black border border-green-800 rounded-lg px-3 py-2 text-sm text-green-300 focus:outline-none focus:ring-2 focus:ring-green-600" />
          </div>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1 text-green-400">Pad (optional)</label>
          <select name="padSlug" defaultValue={defaultPad} className="w-full bg-black border border-green-800 rounded-lg px-3 py-2 text-sm text-green-300 focus:outline-none focus:ring-2 focus:ring-green-600">
            <option value="">No Pad</option>
            {pads.map((p: { slug: string; name: string }) => (
              <option key={p.slug} value={p.slug}>{p.name}</option>
            ))}
          </select>
        </div>
        <label className="flex items-center gap-2 text-sm text-green-400">
          <input name="private" type="checkbox" defaultChecked className="rounded border-green-800 bg-black" />
          Private event
        </label>
        <button type="submit" disabled={loading}
          className={cn('px-4 py-2 bg-green-700 hover:bg-green-600 text-black text-sm rounded-lg transition-colors', loading && 'opacity-60')}
        >
          {loading ? 'Creating…' : 'Create Event'}
        </button>
      </form>
    </div>
  );
}
