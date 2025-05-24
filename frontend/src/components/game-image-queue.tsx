import Image from "next/image"
import type { Game } from "@/lib/types";

interface GameImageQueueProps {
  games: Game[];
}

export default function GameImageQueue({ games }: GameImageQueueProps) {
  const displayedGames = games.slice(0, 4);
  return (
    <div className="flex justify-center items-center relative">
      {displayedGames.map((game, idx) => (
        <div
          key={game.appid}
          className="relative transition-transform duration-200"
          style={{
            zIndex: games.length - idx,
            marginLeft: idx === 0 ? 0 : -60,
          }}
        >
          <div className="relative ring">
            <Image
              src={game.headerImage}
              alt="test"
              width={600 * (1 - idx * 0.1)}
              height={400 * (1 - idx * 0.1)}
              className="rounded-xs"
            />
            <div className="absolute inset-0 bg-black/40 rounded-xs"></div>
          </div>
        </div>
      ))}
    </div>
  );
}
