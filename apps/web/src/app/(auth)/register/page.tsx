'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useMutation } from 'urql';
import { REGISTER_MUTATION } from '@/gql/hoppers';
import { cn } from '@/lib/utils';

export default function RegisterPage() {
  const router = useRouter();
  const [, register] = useMutation(REGISTER_MUTATION);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    const fd = new FormData(e.currentTarget);
    const result = await register({
      username: fd.get('username') as string,
      email: fd.get('email') as string,
      password: fd.get('password') as string,
    });
    setLoading(false);
    if (result.error) {
      setError(result.error.graphQLErrors[0]?.message ?? result.error.message);
      return;
    }
    router.push('/settings');
    router.refresh();
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-pond-50">
      <div className="w-full max-w-sm bg-white rounded-2xl shadow p-8 space-y-6">
        <div className="text-center">
          <span className="text-4xl">🐸</span>
          <h1 className="text-2xl font-bold mt-2">Join the Pond</h1>
        </div>
        {error && (
          <p className="text-sm text-red-600 bg-red-50 rounded px-3 py-2">{error}</p>
        )}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1" htmlFor="username">Username</label>
            <input id="username" name="username" required autoComplete="username"
              className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-pond-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1" htmlFor="email">Email</label>
            <input id="email" name="email" type="email" required autoComplete="email"
              className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-pond-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1" htmlFor="password">Password</label>
            <input id="password" name="password" type="password" required autoComplete="new-password"
              className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-pond-500"
            />
          </div>
          <button type="submit" disabled={loading}
            className={cn(
              'w-full bg-pond-600 hover:bg-pond-700 text-white font-medium py-2 rounded-lg transition-colors',
              loading && 'opacity-60 cursor-not-allowed'
            )}
          >
            {loading ? 'Creating account…' : 'Create Account'}
          </button>
        </form>
        <p className="text-center text-sm text-gray-500">
          Already a Hopper?{' '}
          <a href="/login" className="text-pond-600 hover:underline font-medium">Login</a>
        </p>
      </div>
    </div>
  );
}
