import { NextRequest, NextResponse } from 'next/server';

const REFRESH_MUTATION = `
  mutation RefreshToken {
    refreshToken { accessToken hopper { id username slug anonymous } }
  }
`;

export async function POST(req: NextRequest) {
  const apiUrl = process.env.INTERNAL_API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? '';
  const djangoRes = await fetch(apiUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Cookie: req.headers.get('cookie') ?? '',
    },
    body: JSON.stringify({ query: REFRESH_MUTATION }),
  });
  const data = await djangoRes.json();
  const nextRes = NextResponse.json(data);
  djangoRes.headers.forEach((value, key) => {
    if (key.toLowerCase() === 'set-cookie') {
      nextRes.headers.append('Set-Cookie', value);
    }
  });
  return nextRes;
}
