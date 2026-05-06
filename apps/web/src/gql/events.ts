const EVENT_FRAGMENT = `
  fragment EventFields on EventType {
    id title text start end private active slug createdAt
    pad { id name slug }
    createdBy { id username slug }
    attending { id username slug }
  }
`;

export const EVENTS_QUERY = `
  query Events {
    events { ...EventFields }
  }
  ${EVENT_FRAGMENT}
`;

export const EVENT_QUERY = `
  query Event($slug: String!) {
    event(slug: $slug) { ...EventFields }
  }
  ${EVENT_FRAGMENT}
`;

export const CREATE_EVENT_MUTATION = `
  mutation CreateEvent(
    $title: String!, $text: String, $start: String, $end: String,
    $padSlug: String, $private: Boolean
  ) {
    createEvent(title: $title, text: $text, start: $start, end: $end, padSlug: $padSlug, private: $private) {
      ...EventFields
    }
  }
  ${EVENT_FRAGMENT}
`;

export const UPDATE_EVENT_MUTATION = `
  mutation UpdateEvent(
    $slug: String!, $title: String, $text: String,
    $start: String, $end: String, $private: Boolean
  ) {
    updateEvent(slug: $slug, title: $title, text: $text, start: $start, end: $end, private: $private) {
      ...EventFields
    }
  }
  ${EVENT_FRAGMENT}
`;

export const DELETE_EVENT_MUTATION = `
  mutation DeleteEvent($slug: String!) {
    deleteEvent(slug: $slug)
  }
`;

export const RSVP_EVENT_MUTATION = `
  mutation RsvpEvent($slug: String!) {
    rsvpEvent(slug: $slug) { ...EventFields }
  }
  ${EVENT_FRAGMENT}
`;
