'use client';

import { useMutation } from 'urql';
import { LIKE_RIBBIT_MUTATION, SPOT_RIBBIT_MUTATION, ECHO_RIBBIT_MUTATION } from '@/gql/ribbits';
import { cn } from '@/lib/utils';

interface Props {
  slug: string;
  likeCount: number;
  spotCount: number;
  echoCount: number;
  myId: string;
  likedBy: { id: string }[];
  spottedBy: { id: string }[];
  isMine: boolean;
}

export function RibbitActions({ slug, likeCount, spotCount, echoCount, myId, likedBy, spottedBy, isMine }: Props) {
  const [likeResult, like] = useMutation(LIKE_RIBBIT_MUTATION);
  const [spotResult, spot] = useMutation(SPOT_RIBBIT_MUTATION);
  const [echoResult, echo] = useMutation(ECHO_RIBBIT_MUTATION);

  const liked = likedBy.some((h) => h.id === myId);
  const spotted = spottedBy.some((h) => h.id === myId);

  return (
    <div className="flex items-center gap-4 mt-2 text-sm text-green-700">
      <button
        onClick={() => like({ slug })}
        disabled={likeResult.fetching}
        className={cn('flex items-center gap-1 hover:text-green-400 transition-colors', liked && 'text-green-400 font-medium')}
      >
        👍 {likeCount}
      </button>
      <button
        onClick={() => spot({ slug })}
        disabled={spotResult.fetching}
        className={cn('flex items-center gap-1 hover:text-yellow-400 transition-colors', spotted && 'text-yellow-400 font-medium')}
      >
        🔦 {spotCount}
      </button>
      {!isMine && (
        <button
          onClick={() => echo({ slug })}
          disabled={echoResult.fetching}
          className="flex items-center gap-1 hover:text-blue-400 transition-colors"
        >
          🔁 Echo ({echoCount})
        </button>
      )}
    </div>
  );
}
