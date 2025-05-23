import type { Game } from "@/lib/types";
import { getServerSession } from "next-auth/next";
import GameImageQueue from "@/components/game-image-queue";
import DiscoveryQueueButton from "@/components/discovery-queue-button";

export default async function Page() {
  const session = await getServerSession();
  let games: Game[] = [];
  if (session) {
    const steamId = session.user.email?.slice(0, 17);
    const data = await fetch(
      `http://127.0.0.1:8000/recommendations?steam_id=${steamId}`
    );
    games = await data.json();
  }

  return (
    <div className="min-h-screen bg-gradient-to-r from-neutral-950 to-neutral-800">
      <div className="container mx-auto px-4 py-4">
        <div className="grid gap-2 justify-center">
          <span className="text-4xl font-bald">YOUR DISCOVERY QUEUE</span>
          <span className="text-lg">
            Your recommendations are a mix of products that are similar to what
            you play on Steam.
            <br />
            Click below to get started, use the controls on each product page to
            like or dislike it as your recommendations. <br />
            Or jump to the next title in your queue.
          </span>
          <div className="my-2">
            <span className="text-lg font-bold">YOUR QUEUE</span>
            <GameImageQueue games={games} />
          </div>
          <DiscoveryQueueButton />
        </div>
      </div>
    </div>
  );
}
