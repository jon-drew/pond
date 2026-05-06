import { createClient, cacheExchange, fetchExchange } from '@urql/core';
import { cookies } from 'next/headers';

export async function makeServerClient() {
  const cookieStore = await cookies();
  const cookieHeader = cookieStore
    .getAll()
    .map((c) => `${c.name}=${c.value}`)
    .join('; ');

  return createClient({
    url: process.env.INTERNAL_API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? '',
    fetchOptions: {
      headers: { Cookie: cookieHeader },
      credentials: 'include',
    },
    exchanges: [cacheExchange, fetchExchange],
  });
}
