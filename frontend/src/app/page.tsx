"use client";

import { Button } from "@/components/ui/button";
import { signIn, signOut } from "next-auth/react";
import { useSession } from "next-auth/react";

export default function Home() {
  const session = useSession();

  if (session.status === "authenticated") {
    return (
      <div className="h-screen flex items-center justify-center">
        <Button
          onClick={() => {
            signOut();
          }}
        >
          Sign out
        </Button>
      </div>
    );
  }

  return (
    <div className="h-screen flex items-center justify-center">
      <Button
        onClick={() => {
          signIn("steam");
        }}
      >
        Sign in with Steam
      </Button>
    </div>
  );
}
