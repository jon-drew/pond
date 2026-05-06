import { redirect } from 'next/navigation';
import { cookies } from 'next/headers';
import { makeServerClient } from '@/lib/urql/client';
import { ME_QUERY } from '@/gql/hoppers';
import { ACCESS_TOKEN_COOKIE } from '@/lib/auth';
import { Navbar } from '@/components/layout/navbar';

export default async function AppLayout({ children }: { children: React.ReactNode }) {
  const cookieStore = await cookies();
  if (!cookieStore.has(ACCESS_TOKEN_COOKIE)) {
    redirect('/login');
  }

  const client = await makeServerClient();
  const result = await client.query(ME_QUERY, {});

  if (!result.data?.me) {
    redirect('/login');
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar me={result.data.me} />
      <main className="max-w-4xl mx-auto px-4 py-6">{children}</main>
    </div>
  );
}
