"use client";

import { Button } from "@/components/ui/button";
import { ChevronRight } from "lucide-react";
import { useRouter } from "next/navigation";
export default function DiscoveryQueueButton({appid}: {appid: string}) {
  const router = useRouter();
  return (
    <Button
      className="group text-xl py-5 bg-gradient-to-r from-neutral-950 to-neutral-50 hover:from-neutral-500 hover:to-neutral-50 flex justify-end"
      onClick={() => {
        router.push(`/recommendations/${appid}`);
      }}
    >
      Click here to begin exploring your queue
      <ChevronRight className="mt-1 group-hover:translate-x-1 transition-transform" />
    </Button>
  );
}
