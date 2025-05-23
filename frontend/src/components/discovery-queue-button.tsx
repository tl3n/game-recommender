"use client";

import { Button } from "@/components/ui/button";
import { ChevronRight } from "lucide-react";
export default function DiscoveryQueueButton() {
  return (
    <Button
      className="group text-xl py-5 bg-gradient-to-r from-neutral-950 to-neutral-50 hover:from-neutral-500 hover:to-neutral-50 flex justify-end"
      onClick={() => {
        console.log("button is clicked");
      }}
    >
      Click here to begin exploring your queue
      <ChevronRight className="mt-1 group-hover:translate-x-1 transition-transform" />
    </Button>
  );
}
