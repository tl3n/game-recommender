import { NextResponse } from "next/server";

export async function POST(request: Request) {
  const { appid, status, steamid } = await request.json();
  
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/games/${appid}/status`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ status, steamid }),
  });

  if (!response.ok) {
    return NextResponse.json({ error: 'Failed to update game status' }, { status: 500 });
  }
  
  return NextResponse.json({ success: true });
}