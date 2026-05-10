'use client';

import { useState } from 'react';
import { useQuery, useMutation } from 'urql';
import { ME_QUERY, UPDATE_HOPPER_MUTATION } from '@/gql/hoppers';
import { cn } from '@/lib/utils';

export default function SettingsPage() {
  const [meResult] = useQuery({ query: ME_QUERY });
  const [, updateHopper] = useMutation(UPDATE_HOPPER_MUTATION);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const me = meResult.data?.me;

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError(null);
    const fd = new FormData(e.currentTarget);
    const result = await updateHopper({
      name: fd.get('name') as string || null,
      email: fd.get('email') as string || null,
      birthDate: fd.get('birthDate') as string || null,
    });
    if (result.error) {
      setError(result.error.graphQLErrors[0]?.message ?? result.error.message);
      return;
    }
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  }

  if (!me) return <p className="text-gray-400">Loading…</p>;

  return (
    <div className="max-w-md space-y-6">
      <h1 className="text-xl font-bold">Settings</h1>
      {me.anonymous && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-4 text-sm text-yellow-800">
          <strong>You're anonymous.</strong> Fill in your name, email, and birthday to go public and appear to other Hoppers.
        </div>
      )}
      <form onSubmit={handleSubmit} className="bg-white rounded-2xl border border-gray-200 p-6 space-y-4">
        {error && <p className="text-sm text-red-600">{error}</p>}
        <div>
          <label className="block text-sm font-medium mb-1">Display Name</label>
          <input name="name" defaultValue={me.name} placeholder="Your name"
            className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-pond-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Email</label>
          <input name="email" type="email" defaultValue={me.email} placeholder="you@example.com"
            className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-pond-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Birthday</label>
          <input name="birthDate" type="date"
            className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-pond-500"
          />
        </div>
        <button type="submit"
          className={cn('px-4 py-2 bg-pond-600 hover:bg-pond-700 text-white text-sm rounded-lg transition-colors', saved && 'bg-green-600')}
        >
          {saved ? '✓ Saved' : 'Save Changes'}
        </button>
      </form>
    </div>
  );
}
