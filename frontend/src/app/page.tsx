"use client";

import { Button } from "@/components/ui/button";
import { ChevronRight } from "lucide-react";
import { signIn, useSession } from "next-auth/react";
import { useRouter, useSearchParams } from "next/navigation";

export default function Home() {
  const session = useSession();
  const router = useRouter();
  const searchParams = useSearchParams();
  const callbackUrl = searchParams.get("callbackUrl") || "/recommendations";

  return (
    <div className="flex items-center justify-center mt-60">
      <div className="grid text-center">
        <span className="text-6xl font-bold">
          DISCOVER YOUR NEXT <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-stone-300 to-stone-500">
            FAVOURITE GAME
          </span>
        </span>
        <div className="my-4">
          <span className="text-lg">
            Get personalized game recommendations powered by machine learning.{" "}
            <br />
            Find games you'll love based on your preferences and playing
            history.
          </span>
        </div>
        <div className="">
          <Button
            variant="outline"
            className="group bg-transparent text-xl px-5 py-5"
            onClick={() => {
              if (session.status === "authenticated") {
                router.push(callbackUrl);
              } else {
                signIn("steam", { callbackUrl });
              }
            }}
          >
            {session.status === "authenticated" ? "Go to your discovery queue" : "Sign in with steam"}
            <ChevronRight className="mt-1 group-hover:translate-x-1 transition-transform" />
          </Button>
        </div>
      </div>
    </div>
  );
}
