'use client';

import { createClient, cacheExchange, fetchExchange, Provider } from 'urql';
import { authExchange } from '@urql/exchange-auth';
import { ReactNode, useMemo } from 'react';

const REFRESH_MUTATION = `
  mutation RefreshToken {
    refreshToken {
      accessToken
      hopper { id username slug anonymous }
    }
  }
`;

function makeClient() {
  return createClient({
    url: '/api/graphql',
    fetchOptions: { credentials: 'include' },
    exchanges: [
      cacheExchange,
      authExchange(async (utilities) => ({
        addAuthToOperation(operation) {
          return operation;
        },
        didAuthError(error) {
          return error.graphQLErrors.some(
            (e) => e.extensions?.['code'] === 'UNAUTHENTICATED' ||
                   (e.message ?? '').toLowerCase().includes('authentication required')
          );
        },
        async refreshAuth() {
          await utilities.mutate(REFRESH_MUTATION, {});
        },
      })),
      fetchExchange,
    ],
  });
}

export function UrqlProvider({ children }: { children: ReactNode }) {
  const client = useMemo(() => makeClient(), []);
  return <Provider value={client}>{children}</Provider>;
}
