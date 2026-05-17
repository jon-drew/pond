import { makeServerClient } from '@/lib/urql/client';
import { HOPPERS_QUERY } from '@/gql/hoppers';
import { HoppersList } from './hoppers-list';

export default async function HoppersPage() {
  const client = await makeServerClient();
  const result = await client.query(HOPPERS_QUERY, {});
  const hoppers = result.data?.hoppers ?? [];

  return <HoppersList hoppers={hoppers} />;
}
