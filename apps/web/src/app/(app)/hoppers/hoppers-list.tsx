'use client';

import { useState } from 'react';
import Link from 'next/link';

interface Hopper {
  id: string;
  username: string;
  name: string;
  slug: string;
  anonymous: boolean;
}

export function HoppersList({ hoppers }: { hoppers: Hopper[] }) {
  const [search, setSearch] = useState('');
  const q = search.trim().toLowerCase();
  const filtered = q
    ? hoppers.filter(
        (h) =>
          h.username.toLowerCase().includes(q) ||
          (h.name && h.name.toLowerCase().includes(q)),
      )
    : hoppers;

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-bold text-green-400">Hoppers</h1>
      <input
        type="search"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        placeholder="Search hoppers…"
        className="w-full bg-black border border-green-800 rounded-lg px-3 py-2 text-sm text-green-300 placeholder-green-900 focus:outline-none focus:ring-2 focus:ring-green-600"
      />
      <div className="grid gap-3">
        {filtered.map((h) => (
          <Link
            key={h.id}
            href={`/hoppers/${h.slug}`}
            className="bg-black rounded-xl border border-green-800 p-4 flex items-center gap-3 hover:border-green-600 transition-colors"
          >
            <span className="text-2xl">🐸</span>
            <div>
              <p className="font-medium">{h.name || h.username}</p>
              <p className="text-xs text-green-700">@{h.username}</p>
            </div>
          </Link>
        ))}
        {filtered.length === 0 && (
          <div className="text-center py-12">
            <p className="text-4xl mb-3">🐸</p>
            <p className="text-green-700 text-sm">
              {search ? `No hoppers matching "${search}"` : 'The pond is empty.'}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
