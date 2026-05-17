'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useMutation } from 'urql';
import { LOGIN_MUTATION } from '@/gql/hoppers';
import { cn } from '@/lib/utils';

export default function LoginPage() {
  const router = useRouter();
  const [, login] = useMutation(LOGIN_MUTATION);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    const fd = new FormData(e.currentTarget);
    const result = await login({
      username: fd.get('username') as string,
      password: fd.get('password') as string,
    });
    setLoading(false);
    if (result.error) {
      setError(result.error.graphQLErrors[0]?.message ?? result.error.message);
      return;
    }
    router.push('/ribbits');
    router.refresh();
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-black">
      <div className="w-full max-w-sm bg-black rounded-2xl border border-green-800 p-8 space-y-6">
        <div className="text-center">
          <span className="text-4xl">🐸</span>
          <h1 className="text-2xl font-bold mt-2 text-green-400">Hop In</h1>
        </div>
        {error && (
          <p className="text-sm text-red-400 bg-red-950 border border-red-800 rounded px-3 py-2">{error}</p>
        )}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1 text-green-400" htmlFor="username">Username</label>
            <input
              id="username" name="username" required autoComplete="username"
              className="w-full bg-black border border-green-800 rounded-lg px-3 py-2 text-sm text-green-300 placeholder-green-900 focus:outline-none focus:ring-2 focus:ring-green-600"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1 text-green-400" htmlFor="password">Password</label>
            <input
              id="password" name="password" type="password" required autoComplete="current-password"
              className="w-full bg-black border border-green-800 rounded-lg px-3 py-2 text-sm text-green-300 placeholder-green-900 focus:outline-none focus:ring-2 focus:ring-green-600"
            />
          </div>
          <button
            type="submit" disabled={loading}
            className={cn(
              'w-full bg-green-700 hover:bg-green-600 text-black font-medium py-2 rounded-lg transition-colors',
              loading && 'opacity-60 cursor-not-allowed'
            )}
          >
            {loading ? 'Logging in…' : 'Login'}
          </button>
        </form>
        <p className="text-center text-sm text-green-700">
          New here?{' '}
          <a href="/register" className="text-green-400 hover:text-green-300 font-medium">Register</a>
        </p>
      </div>
    </div>
  );
}
