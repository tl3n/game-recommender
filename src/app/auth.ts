import type { AuthOptions } from 'next-auth'
import Steam, { STEAM_PROVIDER_ID } from 'next-auth-steam'
import type { NextRequest } from 'next/server'

export function getAuthOptions(req?: NextRequest): AuthOptions {
  return {
    providers: req
      ? [
          Steam(req, {
            clientSecret: process.env.STEAM_API_KEY!
          })
        ]
      : [],
    callbacks: {
      jwt({ token, account, profile }) {
        if (account?.provider === STEAM_PROVIDER_ID) {
          token.steam = profile
        }

        return token
      },
      session({ session, token }) {
        if ('steam' in token) {
          session.user!.steam = token.steam
        }

        return session
      }
    }
  }
}