export const HOPPER_FRAGMENT = `
  fragment HopperFields on HopperType {
    id username email name anonymous slug createdAt
  }
`;

export const ME_QUERY = `
  query Me {
    me { ...HopperFields }
  }
  ${HOPPER_FRAGMENT}
`;

export const HOPPERS_QUERY = `
  query Hoppers {
    hoppers { ...HopperFields }
  }
  ${HOPPER_FRAGMENT}
`;

export const HOPPER_QUERY = `
  query Hopper($slug: String!) {
    hopper(slug: $slug) { ...HopperFields }
  }
  ${HOPPER_FRAGMENT}
`;

export const LOGIN_MUTATION = `
  mutation Login($username: String!, $password: String!) {
    login(username: $username, password: $password) {
      accessToken
      hopper { ...HopperFields }
    }
  }
  ${HOPPER_FRAGMENT}
`;

export const REGISTER_MUTATION = `
  mutation Register($username: String!, $email: String!, $password: String!) {
    register(username: $username, email: $email, password: $password) {
      accessToken
      hopper { ...HopperFields }
    }
  }
  ${HOPPER_FRAGMENT}
`;

export const REFRESH_TOKEN_MUTATION = `
  mutation RefreshToken {
    refreshToken {
      accessToken
      hopper { ...HopperFields }
    }
  }
  ${HOPPER_FRAGMENT}
`;

export const LOGOUT_MUTATION = `
  mutation Logout {
    logout
  }
`;

export const UPDATE_HOPPER_MUTATION = `
  mutation UpdateHopper($name: String, $email: String, $birthDate: String) {
    updateHopper(name: $name, email: $email, birthDate: $birthDate) {
      ...HopperFields
    }
  }
  ${HOPPER_FRAGMENT}
`;

export const FOLLOW_HOPPER_MUTATION = `
  mutation FollowHopper($slug: String!) {
    followHopper(slug: $slug) { ...HopperFields }
  }
  ${HOPPER_FRAGMENT}
`;
