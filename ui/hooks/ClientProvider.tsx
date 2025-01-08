"use client";

import React from "react";
import { UserProvider } from "@/hooks/UserContext";

export default function ClientProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  return <UserProvider>{children}</UserProvider>;
}
