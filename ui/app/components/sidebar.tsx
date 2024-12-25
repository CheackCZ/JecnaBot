import React from "react"; // Import React for creating components.

// Sidebar component: The main container for the sidebar.
export function Sidebar({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    // Renders an `aside` element with full height and additional custom classes.
    <aside className={`h-full ${className}`}>{children}</aside>
  );
}

// SidebarHeader component: Represents the header section of the sidebar.
export function SidebarHeader({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    // Renders a `div` with padding and a bottom border for the header section.
    <div className={`p-4 border-b ${className}`}>{children}</div>
  );
}

// SidebarContent component: Represents the main content area of the sidebar.
export function SidebarContent({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    // Renders a flexible `div` with padding, allowing for expandable content.
    <div className={`flex-1 p-4 ${className}`}>{children}</div>
  );
}

// SidebarGroup component: Used to group related items within the sidebar.
export function SidebarGroup({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    // Renders a `div` with bottom margin for grouping items together.
    <div className={`mb-6 ${className}`}>{children}</div>
  );
}

// SidebarFooter component: Represents the footer section of the sidebar.
export function SidebarFooter({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    // Renders a `div` with padding and a top border for the footer section.
    <div className={`p-4 border-t ${className}`}>{children}</div>
  );
}