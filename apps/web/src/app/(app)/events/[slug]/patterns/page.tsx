import { redirect } from 'next/navigation';
import { makeServerClient } from '@/lib/urql/client';
import { ME_QUERY } from '@/gql/hoppers';
import { EVENT_QUERY } from '@/gql/events';
import { EVENT_RIBBIT_PATTERN_QUERY } from '@/gql/ribbits';
import { RibbitPatternTree } from '@/components/ribbits/ribbit-pattern-tree';
import { format } from 'date-fns';
import Link from 'next/link';

interface PatternNode {
  ribbit: { id: string; createdAt: string; sentBy: { username: string } };
  parentSlug: string | null;
  depth: number;
  directEchoCount: number;
  totalEchoCount: number;
  score: number;
}

export default async function PatternsPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const client = await makeServerClient();
  const [meResult, eventResult] = await Promise.all([
    client.query(ME_QUERY, {}),
    client.query(EVENT_QUERY, { slug }),
  ]);

  const me = meResult.data?.me;
  const event = eventResult.data?.event;

  if (!event) return redirect(`/events`);
  if (!me || me.id !== event.createdBy?.id) return redirect(`/events/${slug}`);

  const patternResult = await client.query(EVENT_RIBBIT_PATTERN_QUERY, { eventSlug: slug });
  const nodes = patternResult.data?.eventRibbitPattern ?? [];

  const byTime = [...nodes as PatternNode[]].sort(
    (a, b) => new Date(a.ribbit.createdAt).getTime() - new Date(b.ribbit.createdAt).getTime()
  );
  const byReach = [...nodes as PatternNode[]].sort((a, b) => b.totalEchoCount - a.totalEchoCount);

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <Link href={`/events/${slug}`} className="text-sm text-green-700 hover:text-green-400">← {event.title}</Link>
          <h1 className="text-xl font-bold mt-1 text-green-400">Ribbit Patterns</h1>
          <p className="text-sm text-green-700">{nodes.length} Ribbits · {nodes.filter((n: PatternNode) => n.parentSlug !== null).length} echoes</p>
        </div>
      </div>

      <section className="space-y-3">
        <h2 className="font-semibold text-base text-green-400">Echo Tree</h2>
        <p className="text-xs text-green-700">Shows who Ribbited because of whom. Expand nodes to see the chain.</p>
        <RibbitPatternTree nodes={nodes} />
      </section>

      <section className="space-y-3">
        <h2 className="font-semibold text-base text-green-400">Timeline</h2>
        <div className="space-y-2">
          {byTime.map((n) => (
            <div key={n.ribbit.id} className="bg-black rounded-lg border border-green-900 px-4 py-2 flex items-center justify-between text-sm">
              <div className="flex items-center gap-3">
                <span className="text-xs text-green-700 w-32 shrink-0">
                  {format(new Date(n.ribbit.createdAt), 'MMM d, h:mm a')}
                </span>
                <span className="font-medium">@{n.ribbit.sentBy.username}</span>
                {n.parentSlug && <span className="text-xs text-blue-400">🔁 echo</span>}
              </div>
              <span className="text-xs text-green-700">depth {n.depth}</span>
            </div>
          ))}
        </div>
      </section>

      <section className="space-y-3">
        <h2 className="font-semibold text-base text-green-400">Leaderboard — Most Echoed</h2>
        <div className="space-y-2">
          {byReach.slice(0, 10).map((n, i) => (
            <div key={n.ribbit.id} className="bg-black rounded-lg border border-green-900 px-4 py-2 flex items-center justify-between text-sm">
              <div className="flex items-center gap-3">
                <span className="text-green-700 w-5">#{i + 1}</span>
                <span className="font-medium">@{n.ribbit.sentBy.username}</span>
              </div>
              <div className="flex items-center gap-4 text-xs text-green-700">
                <span>Score: {n.score}</span>
                <span>Direct: {n.directEchoCount}</span>
                <span className="font-medium text-green-400">Total reach: {n.totalEchoCount}</span>
              </div>
            </div>
          ))}
          {nodes.length === 0 && <p className="text-green-700 text-sm">No Ribbits yet.</p>}
        </div>
      </section>
    </div>
  );
}
