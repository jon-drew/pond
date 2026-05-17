'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useMutation } from 'urql';
import { REGISTER_MUTATION } from '@/gql/hoppers';
import { cn, formatAuthError } from '@/lib/utils';

export default function RegisterPage() {
  const router = useRouter();
  const [, register] = useMutation(REGISTER_MUTATION);
  const [error, setError] = useState<{ friendly: string; debug: string } | null>(null);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

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
      setError(formatAuthError(result.error));
      return;
    }
    setSuccess(true);
    setTimeout(() => router.push('/login'), 1500);
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-black">
      <div className="w-full max-w-sm bg-black rounded-2xl border border-green-800 p-8 space-y-6">
        <div className="text-center">
          <span className="text-4xl">🐸</span>
          <h1 className="text-2xl font-bold mt-2 text-green-400">Join the Pond</h1>
        </div>
        {error && (
          <div className="text-sm text-red-400 bg-red-950 border border-red-800 rounded px-3 py-2">
            <p>{error.friendly}</p>
            <p className="text-xs text-red-800 mt-1">[{error.debug}]</p>
          </div>
        )}
        {success && (
          <p className="text-sm text-green-400 bg-green-950 border border-green-800 rounded px-3 py-2">Account created! Redirecting to login…</p>
        )}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1 text-green-400" htmlFor="username">Username</label>
            <input id="username" name="username" required autoComplete="username"
              className="w-full bg-black border border-green-800 rounded-lg px-3 py-2 text-sm text-green-300 placeholder-green-900 focus:outline-none focus:ring-2 focus:ring-green-600"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1 text-green-400" htmlFor="email">Email</label>
            <input id="email" name="email" type="email" required autoComplete="email"
              className="w-full bg-black border border-green-800 rounded-lg px-3 py-2 text-sm text-green-300 placeholder-green-900 focus:outline-none focus:ring-2 focus:ring-green-600"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1 text-green-400" htmlFor="password">Password</label>
            <input id="password" name="password" type="password" required autoComplete="new-password"
              className="w-full bg-black border border-green-800 rounded-lg px-3 py-2 text-sm text-green-300 placeholder-green-900 focus:outline-none focus:ring-2 focus:ring-green-600"
            />
          </div>
          <button type="submit" disabled={loading}
            className={cn(
              'w-full bg-green-700 hover:bg-green-600 text-black font-medium py-2 rounded-lg transition-colors',
              loading && 'opacity-60 cursor-not-allowed'
            )}
          >
            {loading ? 'Creating account…' : 'Create Account'}
          </button>
        </form>
        <p className="text-center text-sm text-green-700">
          Already a Hopper?{' '}
          <a href="/login" className="text-green-400 hover:text-green-300 font-medium">Login</a>
        </p>
      </div>
    </div>
  );
}
