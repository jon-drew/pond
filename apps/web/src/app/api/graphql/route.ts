import { NextRequest, NextResponse } from 'next/server';

const API_URL = process.env.INTERNAL_API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? '';

export async function POST(req: NextRequest) {
  if (!API_URL || API_URL.includes('<') || API_URL.includes('>')) {
    return NextResponse.json(
      { errors: [{ message: 'INTERNAL_API_URL is not set to a real URL — go to Railway → web service → Variables and set it to your actual API service domain [missing-env:INTERNAL_API_URL]' }] },
      { status: 503 },
    );
  }

  const target = API_URL.endsWith('/graphql/') ? API_URL : `${API_URL.replace(/\/$/, '')}/graphql/`;

  let djangoRes: Response;
  try {
    djangoRes = await fetch(target, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Cookie: req.headers.get('cookie') ?? '',
      },
      body: await req.text(),
    });
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    return NextResponse.json(
      { errors: [{ message: `API unreachable [fetch-failed:${msg}]` }] },
      { status: 503 },
    );
  }

  const data = await djangoRes.text();

  // If Django returned non-JSON (e.g. an HTML error page), surface it clearly
  const isJson = djangoRes.headers.get('content-type')?.includes('application/json');
  if (!isJson) {
    return NextResponse.json(
      { errors: [{ message: `API returned non-JSON [status:${djangoRes.status}]` }] },
      { status: 502 },
    );
  }

  const res = new NextResponse(data, {
    status: djangoRes.status,
    headers: { 'Content-Type': 'application/json' },
  });

  djangoRes.headers.forEach((value, key) => {
    if (key.toLowerCase() === 'set-cookie') res.headers.append('Set-Cookie', value);
  });

  return res;
}
