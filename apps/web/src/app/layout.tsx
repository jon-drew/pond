import type { Metadata } from 'next';
import './globals.css';
import { UrqlProvider } from '@/lib/urql/client-provider';

export const metadata: Metadata = {
  title: 'Pond',
  description: 'The frog social network',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-black text-green-300">
        <UrqlProvider>{children}</UrqlProvider>
      </body>
    </html>
  );
}
