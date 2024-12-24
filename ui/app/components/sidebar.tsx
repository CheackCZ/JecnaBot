import React from "react";

export function Sidebar({ children, className }: { children: React.ReactNode; className?: string }) {
  return <aside className={`h-full ${className}`}>{children}</aside>;
}

export function SidebarHeader({ children, className }: { children: React.ReactNode; className?: string }) {
  return <div className={`p-4 border-b ${className}`}>{children}</div>;
}

export function SidebarContent({ children, className }: { children: React.ReactNode; className?: string }) {
  return <div className={`flex-1 p-4 ${className}`}>{children}</div>;
}

export function SidebarGroup({ children, className }: { children: React.ReactNode; className?: string }) {
  return <div className={`mb-6 ${className}`}>{children}</div>;
}

export function SidebarFooter({ children, className }: { children: React.ReactNode; className?: string }) {
  return <div className={`p-4 border-t ${className}`}>{children}</div>;
}