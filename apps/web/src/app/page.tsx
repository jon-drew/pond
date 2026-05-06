import { redirect } from 'next/navigation';
import { cookies } from 'next/headers';
import { ACCESS_TOKEN_COOKIE } from '@/lib/auth';

export default async function RootPage() {
  const cookieStore = await cookies();
  redirect(cookieStore.has(ACCESS_TOKEN_COOKIE) ? '/ribbits' : '/login');
}
