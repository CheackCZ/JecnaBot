import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
    const token = request.cookies.get("token")?.value;

    // Debug log for verification
    console.log("Middleware triggered for:", request.nextUrl.pathname);
    console.log("Token found:", token);

    // If no token is found, redirect to the login page
    if (!token) {
        return NextResponse.redirect(new URL("/login", request.url));
    }

    return NextResponse.next();
}

export const config = {
    matcher: ["/chat/:path*"], 
};
