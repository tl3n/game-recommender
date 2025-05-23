"use client";

import { Button } from "@/components/ui/button";
import { signIn, signOut } from "next-auth/react";
import { useSession } from "next-auth/react";

export default function Home() {
  const session = useSession();
      // @ts-expect-error - Steam profile added by Steam provider

  console.log(session.data?.user.steam.steamid);
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-neutral-950 to-neutral-800">
      {session.status === "authenticated" ? (
        <Button
          onClick={() => {
            signOut();
          }}
        >
          Sign out
        </Button>
      ) : (
        <Button
          onClick={() => {
            signIn("steam");
          }}
        >
          Sign in with Steam
        </Button>
      )}
    </div>
  );
}
