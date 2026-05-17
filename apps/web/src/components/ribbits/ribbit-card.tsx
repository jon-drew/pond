import { RibbitActions } from './ribbit-actions';
import { formatDistanceToNow } from 'date-fns';

interface Hopper { id: string; username: string; slug: string; }
interface Ribbit {
  id: string; slug: string; createdAt: string; score: number; echoCount: number;
  sentBy: Hopper;
  event: { id: string; title: string; slug: string };
  echoOf: { id: string; slug: string; sentBy: Hopper } | null;
  likes: Hopper[];
  spots: Hopper[];
}

interface Props {
  ribbit: Ribbit;
  myId: string;
}

export function RibbitCard({ ribbit, myId }: Props) {
  return (
    <div className="bg-black rounded-xl border border-green-800 p-4 space-y-2">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-lg">🐸</span>
          <a href={`/hoppers/${ribbit.sentBy.slug}`} className="font-medium text-sm hover:text-green-400">
            {ribbit.sentBy.username}
          </a>
          <span className="text-green-800 text-xs">·</span>
          <a href={`/events/${ribbit.event.slug}`} className="text-xs text-green-700 hover:text-green-400">
            {ribbit.event.title}
          </a>
        </div>
        <span className="text-xs text-green-700">
          {formatDistanceToNow(new Date(ribbit.createdAt), { addSuffix: true })}
        </span>
      </div>
      {ribbit.echoOf && (
        <p className="text-xs text-blue-400">
          🔁 Echo of <a href={`/hoppers/${ribbit.echoOf.sentBy.slug}`} className="hover:underline">@{ribbit.echoOf.sentBy.username}</a>
        </p>
      )}
      <RibbitActions
        slug={ribbit.slug}
        likeCount={ribbit.likes.length}
        spotCount={ribbit.spots.length}
        echoCount={ribbit.echoCount}
        myId={myId}
        likedBy={ribbit.likes}
        spottedBy={ribbit.spots}
        isMine={ribbit.sentBy.id === myId}
      />
      <p className="text-xs text-green-700">Score: {ribbit.score}</p>
    </div>
  );
}
