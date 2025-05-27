"use client";

import { Button } from "@/components/ui/button";
import { signOut } from "next-auth/react";
import { useSession } from "next-auth/react";
import Link from "next/link";
import { Avatar, AvatarImage } from "./ui/avatar";

export default function Header() {
  const session = useSession();
  // @ts-expect-error - Steam profile added by Steam provider
  const avatar = session.data?.user.steam!.avatar;
  const name = session.data?.user.name;
  console.log(session);
  return (
    <header className="bg-neutral-900/30 border-b border-neutral-800">
      <div className="px-4 py-2">
        <div className="flex items-center justify-between">
          <Link href="/" className="text-xl font-bold">
            Game Recommender
          </Link>
          <div className="flex items-center gap-4">
            {session.status === "authenticated" && (
              <div className="flex justify-center gap-2">
                <div className="flex justify-center items-center gap-2">
                  <Avatar>
                    <AvatarImage src={avatar} />
                  </Avatar>
                  <span className="text-sm">{name}</span>
                </div>
                <Button
                  variant="outline"
                  className="bg-transparent"
                  onClick={() => {
                    signOut();
                  }}
                >
                  Sign out
                </Button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
