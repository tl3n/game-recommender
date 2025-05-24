import { withAuth } from "next-auth/middleware";
import { NextResponse } from "next/server";

export default withAuth(
  function middleware(req) {
    if (!req.nextauth.token) {
      const url = new URL("/", req.url);
      url.searchParams.set("callbackUrl", req.nextUrl.pathname);
      return NextResponse.redirect(url);
    }
  },
  {
    callbacks: {
      authorized: ({ token }) => !!token,
    },
    pages: {
      signIn: "/",
    },
  }
);

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - / (home page)
     * - /api (API routes)
     * - /_next (Next.js internals)
     * - /favicon.ico, /sitemap.xml (static files)
     */
    "/((?!api|_next|favicon.ico|sitemap.xml).*)",
  ],
}; 