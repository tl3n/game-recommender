"use client";

import type { Game } from "@/lib/types";
import { Button } from "./ui/button";
import { ThumbsUp, ThumbsDown, ChevronLeft, ChevronRight } from "lucide-react";
import { useRouter } from "next/navigation";
import { useSession } from "next-auth/react";
import { useState } from "react";

interface GameNavigationProps {
  game: Game;
  nextGameId?: string;
  prevGameId?: string;
}

export default function GameNavigation({
  game,
  nextGameId,
  prevGameId,
}: GameNavigationProps) {
  const [status, setStatus] = useState<"liked" | "disliked" | null>(null);

  const router = useRouter();
  const session = useSession();
  // @ts-expect-error - Steam profile added by Steam provider
  const steamid = session?.data?.user.steam.steamid;

  const handleLike = async () => {
    if (status === "liked") {
      setStatus(null);
    } else {
      setStatus("liked");
    }
  };

  const handleDislike = async () => {
    if (status === "disliked") {
      setStatus(null);
    } else {
      setStatus("disliked");
    }
  };

  return (
    <div className="flex justify-between">
      <div className="flex gap-2">
        <Button
          variant="outline"
          className={`w-30 ${
            status === "liked"
              ? "bg-lime-600 hover:bg-lime-800"
              : "bg-transparent"
          }`}
          onClick={handleLike}
        >
          Like <ThumbsUp className="ml-2" />
        </Button>

        <Button
          variant="outline"
          className={`w-30 ${
            status === "disliked"
              ? "bg-red-600 hover:bg-red-800"
              : "bg-transparent"
          }`}
          onClick={handleDislike}
        >
          Dislike <ThumbsDown className="ml-2" />
        </Button>
      </div>
      <div className="flex gap-2">
        {prevGameId && (
          <Button
            variant="outline"
            className="bg-transparent"
            onClick={async () => {
              if (status) {
                await fetch("/api/games/status", {
                  method: "POST",
                  headers: {
                    "Content-Type": "application/json",
                  },
                  body: JSON.stringify({
                    appid: game.appid,
                    status: status,
                    steamid,
                  }),
                });
              }

              router.push(`/recommendations/${prevGameId}`);
            }}
          >
            <ChevronLeft />
          </Button>
        )}
        {nextGameId ? (
          <Button
            variant="outline"
            className="bg-transparent"
            onClick={async () => {
              if (status) {
                await fetch("/api/games/status", {
                  method: "POST",
                  headers: {
                    "Content-Type": "application/json",
                  },
                  body: JSON.stringify({
                    appid: game.appid,
                    status: status,
                    steamid,
                  }),
                });
              }

              router.push(`/recommendations/${nextGameId}`);
            }}
          >
            <ChevronRight />
          </Button>
        ) : (
          <Button
            variant="outline"
            className="bg-transparent"
            onClick={async () => {
              if (status) {
                await fetch("/api/games/status", {
                  method: "POST",
                  headers: {
                    "Content-Type": "application/json",
                  },
                  body: JSON.stringify({
                    appid: game.appid,
                    status: status,
                    steamid,
                  }),
                });
              }

              // Revalidate the recommendations page
              await fetch("/api/revalidate?path=/recommendations", {
                method: "POST",
              });

              router.push("/recommendations/");
            }}
          >
            Finish
          </Button>
        )}
      </div>
    </div>
  );
}
