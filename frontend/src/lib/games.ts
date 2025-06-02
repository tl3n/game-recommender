import { cache } from "react";
import type { Game } from "./types";
import { getServerSession } from "next-auth";

export const getGames = cache(async (): Promise<Game[]> => {
  const session = await getServerSession();
  let steamId = "";
  if (session?.user?.email) {
    steamId = session.user.email.slice(0, 17);
  }
  const data = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/recommendations?steam_id=${steamId}`,
    { next: { revalidate: 3600 } }
  );
  return data.json();
});