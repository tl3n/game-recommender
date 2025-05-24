"use client";

import { Button } from "@/components/ui/button";
import { signOut } from "next-auth/react";
import { useSession } from "next-auth/react";
import Link from "next/link";

export default function Header() {
  const session = useSession();

  return (
    <header className="bg-neutral-900/30 border-b border-neutral-800">
      <div className="px-4 py-2">
        <div className="flex items-center justify-between">
          <Link href="/" className="text-xl font-bold">
            Game Recommender
          </Link>
          <div className="flex items-center gap-4">
            {session.status === "authenticated" && (
              <Button
                variant="ghost"
                onClick={() => {
                  signOut();
                }}
              >
                Sign out
              </Button>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}