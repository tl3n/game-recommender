import { revalidatePath } from "next/cache";
import { NextResponse } from "next/server";

export async function POST(request: Request) {
  const { appid, status, steamid } = await request.json();
  
  const response = await fetch('http://127.0.0.1:8000/game-status', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ appid, status, steamid }),
  });

  if (!response.ok) {
    return NextResponse.json({ error: 'Failed to update game status' }, { status: 500 });
  }
  
  return NextResponse.json({ success: true });
}