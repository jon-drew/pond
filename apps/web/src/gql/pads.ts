const PAD_FRAGMENT = `
  fragment PadFields on PadType {
    id name address description slug createdAt active
    owner { id username slug }
  }
`;

export const PADS_QUERY = `
  query Pads {
    pads { ...PadFields }
  }
  ${PAD_FRAGMENT}
`;

export const PAD_QUERY = `
  query Pad($slug: String!) {
    pad(slug: $slug) { ...PadFields }
  }
  ${PAD_FRAGMENT}
`;

export const CREATE_PAD_MUTATION = `
  mutation CreatePad($name: String!, $address: String!, $description: String!) {
    createPad(name: $name, address: $address, description: $description) {
      ...PadFields
    }
  }
  ${PAD_FRAGMENT}
`;

export const UPDATE_PAD_MUTATION = `
  mutation UpdatePad($slug: String!, $name: String, $address: String, $description: String) {
    updatePad(slug: $slug, name: $name, address: $address, description: $description) {
      ...PadFields
    }
  }
  ${PAD_FRAGMENT}
`;

export const DELETE_PAD_MUTATION = `
  mutation DeletePad($slug: String!) {
    deletePad(slug: $slug)
  }
`;
