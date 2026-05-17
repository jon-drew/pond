'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useMutation } from 'urql';
import { LOGOUT_MUTATION } from '@/gql/hoppers';

interface Me {
  id: string;
  username: string;
  slug: string;
  anonymous: boolean;
}

export function Navbar({ me }: { me: Me }) {
  const router = useRouter();
  const [, logout] = useMutation(LOGOUT_MUTATION);

  async function handleLogout() {
    await logout({});
    router.push('/login');
    router.refresh();
  }

  return (
    <nav className="bg-black border-b border-green-900 sticky top-0 z-10">
      <div className="max-w-4xl mx-auto px-4 h-14 flex items-center justify-between">
        <div className="flex items-center gap-6">
          <Link href="/ribbits" className="text-lg font-bold text-green-400">🐸 Pond</Link>
          <Link href="/ribbits" className="text-sm text-green-700 hover:text-green-400">Ribbits</Link>
          <Link href="/events" className="text-sm text-green-700 hover:text-green-400">Events</Link>
          <Link href="/pads" className="text-sm text-green-700 hover:text-green-400">Pads</Link>
          <Link href="/hoppers" className="text-sm text-green-700 hover:text-green-400">Hoppers</Link>
        </div>
        <div className="flex items-center gap-4">
          <Link href="/settings" className="text-sm text-green-700 hover:text-green-400">
            {me.anonymous ? '(anonymous)' : me.username}
          </Link>
          <button
            onClick={handleLogout}
            className="text-sm text-green-700 hover:text-red-400 transition-colors"
          >
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
}
