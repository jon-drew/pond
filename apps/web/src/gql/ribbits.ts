const RIBBIT_FRAGMENT = `
  fragment RibbitFields on RibbitType {
    id slug createdAt score echoCount
    sentBy { id username slug }
    event { id title slug }
    echoOf { id slug sentBy { id username slug } }
    likes { id username slug }
    spots { id username slug }
  }
`;

export const RIBBITS_QUERY = `
  query Ribbits {
    ribbits { ...RibbitFields }
  }
  ${RIBBIT_FRAGMENT}
`;

export const RIBBIT_QUERY = `
  query Ribbit($slug: String!) {
    ribbit(slug: $slug) { ...RibbitFields }
  }
  ${RIBBIT_FRAGMENT}
`;

export const EVENT_RIBBIT_PATTERN_QUERY = `
  query EventRibbitPattern($eventSlug: String!) {
    eventRibbitPattern(eventSlug: $eventSlug) {
      parentSlug depth directEchoCount totalEchoCount score
      ribbit { ...RibbitFields }
    }
  }
  ${RIBBIT_FRAGMENT}
`;

export const CREATE_RIBBIT_MUTATION = `
  mutation CreateRibbit($eventSlug: String!) {
    createRibbit(eventSlug: $eventSlug) { ...RibbitFields }
  }
  ${RIBBIT_FRAGMENT}
`;

export const LIKE_RIBBIT_MUTATION = `
  mutation LikeRibbit($slug: String!) {
    likeRibbit(slug: $slug) { ...RibbitFields }
  }
  ${RIBBIT_FRAGMENT}
`;

export const SPOT_RIBBIT_MUTATION = `
  mutation SpotRibbit($slug: String!) {
    spotRibbit(slug: $slug) { ...RibbitFields }
  }
  ${RIBBIT_FRAGMENT}
`;

export const ECHO_RIBBIT_MUTATION = `
  mutation EchoRibbit($slug: String!) {
    echoRibbit(slug: $slug) { ...RibbitFields }
  }
  ${RIBBIT_FRAGMENT}
`;
