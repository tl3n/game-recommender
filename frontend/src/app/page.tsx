import { Suspense } from "react";
import DiscoveryButton from "@/components/discovery-button";

export default function Home() {
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
            Find games you&apos;ll love based on your preferences and playing
            history.
          </span>
        </div>
        <div className="">
          <Suspense>
            <DiscoveryButton />
          </Suspense>
        </div>
      </div>
    </div>
  );
}
