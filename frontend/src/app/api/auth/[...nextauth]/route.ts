import { getAuthOptions } from '@/app/auth';
import type { NextRequest } from "next/server";
import NextAuth from 'next-auth';

const handler = async (req: NextRequest, context: { params: Promise<{ nextauth: string[] }> }) => {
  const authOptions = getAuthOptions(req);
  return NextAuth(req, context, authOptions);
};

export { handler as GET, handler as POST };