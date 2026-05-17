import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface GqlError {
  message: string;
  graphQLErrors?: Array<{ message: string }>;
}

export function formatAuthError(err: GqlError): { friendly: string; debug: string } {
  if (err.message.startsWith('[Network]')) {
    const status = err.message.match(/\b([45]\d{2})\b/)?.[1];
    return {
      friendly: 'Could not reach the server. Please try again.',
      debug: `network-error${status ? `:${status}` : ''}`,
    };
  }
  const msg = err.graphQLErrors?.[0]?.message ?? err.message;
  return { friendly: msg, debug: `graphql:${msg}` };
}
