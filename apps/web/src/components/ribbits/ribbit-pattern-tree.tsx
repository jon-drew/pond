'use client';

import { useState } from 'react';
import { formatDistanceToNow } from 'date-fns';

interface PatternNode {
  ribbit: {
    id: string; slug: string; createdAt: string; score: number; echoCount: number;
    sentBy: { id: string; username: string; slug: string };
    event: { id: string; title: string; slug: string };
  };
  parentSlug: string | null;
  depth: number;
  directEchoCount: number;
  totalEchoCount: number;
  score: number;
}

function TreeNode({ node, allNodes, level = 0 }: { node: PatternNode; allNodes: PatternNode[]; level?: number }) {
  const [expanded, setExpanded] = useState(level < 2);
  const children = allNodes.filter((n) => n.parentSlug === node.ribbit.slug);

  return (
    <div className="border-l-2 border-pond-100 pl-3 mt-2">
      <div className="bg-white rounded-lg border border-gray-100 p-3 space-y-1">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-sm">
            <span className="text-base">🐸</span>
            <a href={`/hoppers/${node.ribbit.sentBy.slug}`} className="font-medium hover:text-pond-700">
              {node.ribbit.sentBy.username}
            </a>
            <span className="text-xs text-gray-400">
              {formatDistanceToNow(new Date(node.ribbit.createdAt), { addSuffix: true })}
            </span>
          </div>
          <div className="flex items-center gap-3 text-xs text-gray-500">
            <span>Score: {node.score}</span>
            <span>Direct echoes: {node.directEchoCount}</span>
            <span>Total reach: {node.totalEchoCount}</span>
          </div>
        </div>
        {node.directEchoCount > 0 && (
          <button
            onClick={() => setExpanded(!expanded)}
            className="text-xs text-pond-600 hover:underline"
          >
            {expanded ? '▾ Hide' : '▸ Show'} {node.directEchoCount} echo{node.directEchoCount !== 1 ? 's' : ''}
          </button>
        )}
      </div>
      {expanded && children.map((child) => (
        <TreeNode key={child.ribbit.id} node={child} allNodes={allNodes} level={level + 1} />
      ))}
    </div>
  );
}

export function RibbitPatternTree({ nodes }: { nodes: PatternNode[] }) {
  const roots = nodes.filter((n) => n.parentSlug === null);
  return (
    <div className="space-y-2">
      {roots.map((node) => (
        <TreeNode key={node.ribbit.id} node={node} allNodes={nodes} level={0} />
      ))}
      {roots.length === 0 && (
        <p className="text-gray-400 text-sm">No Ribbits yet for this event.</p>
      )}
    </div>
  );
}
