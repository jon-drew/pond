import { NextRequest, NextResponse } from 'next/server';

const API_URL = process.env.INTERNAL_API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? '';

export async function POST(req: NextRequest) {
  if (!API_URL) {
    return NextResponse.json(
      { errors: [{ message: 'API not configured [missing-env:INTERNAL_API_URL]' }] },
      { status: 503 },
    );
  }

  const target = API_URL.endsWith('/graphql/') ? API_URL : `${API_URL.replace(/\/$/, '')}/graphql/`;

  const djangoRes = await fetch(target, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Cookie: req.headers.get('cookie') ?? '',
    },
    body: await req.text(),
  });

  const data = await djangoRes.text();
  const res = new NextResponse(data, {
    status: djangoRes.status,
    headers: { 'Content-Type': 'application/json' },
  });

  djangoRes.headers.forEach((value, key) => {
    if (key.toLowerCase() === 'set-cookie') res.headers.append('Set-Cookie', value);
  });

  return res;
}
