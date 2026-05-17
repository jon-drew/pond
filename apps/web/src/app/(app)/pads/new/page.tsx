'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useMutation } from 'urql';
import { CREATE_PAD_MUTATION } from '@/gql/pads';
import { cn } from '@/lib/utils';

export default function NewPadPage() {
  const router = useRouter();
  const [, createPad] = useMutation(CREATE_PAD_MUTATION);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    const fd = new FormData(e.currentTarget);
    const result = await createPad({
      name: fd.get('name') as string,
      address: fd.get('address') as string,
      description: fd.get('description') as string,
    });
    setLoading(false);
    if (result.error) { setError(result.error.graphQLErrors[0]?.message ?? result.error.message); return; }
    router.push(`/pads/${result.data.createPad.slug}`);
  }

  return (
    <div className="max-w-md space-y-6">
      <h1 className="text-xl font-bold text-green-400">New Pad</h1>
      <form onSubmit={handleSubmit} className="bg-black rounded-2xl border border-green-800 p-6 space-y-4">
        {error && <p className="text-sm text-red-400 bg-red-950 border border-red-800 rounded px-3 py-2">{error}</p>}
        {(['name', 'address'] as const).map((field) => (
          <div key={field}>
            <label className="block text-sm font-medium mb-1 text-green-400 capitalize">{field}</label>
            <input name={field} required className="w-full bg-black border border-green-800 rounded-lg px-3 py-2 text-sm text-green-300 placeholder-green-900 focus:outline-none focus:ring-2 focus:ring-green-600" />
          </div>
        ))}
        <div>
          <label className="block text-sm font-medium mb-1 text-green-400">Description</label>
          <textarea name="description" rows={3} className="w-full bg-black border border-green-800 rounded-lg px-3 py-2 text-sm text-green-300 placeholder-green-900 focus:outline-none focus:ring-2 focus:ring-green-600" />
        </div>
        <button type="submit" disabled={loading}
          className={cn('px-4 py-2 bg-green-700 hover:bg-green-600 text-black text-sm rounded-lg transition-colors', loading && 'opacity-60')}
        >
          {loading ? 'Creating…' : 'Create Pad'}
        </button>
      </form>
    </div>
  );
}
