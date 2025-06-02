"use client"

import { Button } from "@/components/ui/button";
import { ChevronRight } from "lucide-react";
import { signIn, useSession } from "next-auth/react";
import { useRouter, useSearchParams } from "next/navigation";

export default function DiscoveryButton() {
    const session = useSession();
    const router = useRouter();
    const searchParams = useSearchParams();
    const callbackUrl = searchParams.get("callbackUrl") || "/recommendations";
  
    return (
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
        Go to your discovery queue
        <ChevronRight className="mt-1 group-hover:translate-x-1 transition-transform" />
      </Button>
    );
  }