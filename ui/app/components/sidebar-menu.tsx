"use client";

import React, { useState } from "react"; // Import React and the useState hook for managing component state.
import { useRouter } from "next/navigation"; // Import useRouter for programmatic navigation in Next.js.
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarHeader,
} from "@/app/components/sidebar"; // Import reusable sidebar components.
import { Button } from "@/app/components/button"; // Import the Button component for styling buttons.

export function SidebarMenu() {
  // State for controlling the open/close status of the sidebar.
  const [isOpen, setIsOpen] = useState(true);
  // Router instance for navigation.
  const router = useRouter(); 

  // Toggles the sidebar open/closed state.
  const toggleSidebar = () => setIsOpen(!isOpen);

  // Handles user logout and redirects to the homepage.
  const handleLogout = () => {
    setTimeout(() => {
        router.push("/"); // Redirect to homepage
    }, 0);
  };

  return (
    <div className={`flex ${isOpen ? "w-[14%]" : "w-[4%]"} transition-all`}>

      {/* Sidebar */}
      <Sidebar className={`bg-[#09090B] text-white h-screen flex flex-col ${isOpen ? "border-e border-[#27272A]" : "border-none"}`}>

        {/* Sidebar Header */}
        <SidebarHeader className={`p-4 ${isOpen ? "border-b border-[#27272A]" : "border-none"}`}>
          {isOpen && <img src="/img/Text-white.png" alt="JečnáBot Logo" />}
        </SidebarHeader>

        {/* Sidebar Content */}
        <SidebarContent className="flex-1 p-4 space-y-6 relative">
          {isOpen && (
            <>
              {/* Logout Button */}
              <div className="absolute bottom-0 left-0 w-full p-4">
                <Button className="w-full bg-red-500 hover:bg-red-600 text-white" onClick={handleLogout}>
                  Logout
                </Button>
              </div>
            </>
          )}
        </SidebarContent>

        {/* Sidebar Footer */}
        <SidebarFooter className={`p-4 flex items-center justify-between ${isOpen ? "border-t border-[#27272A]" : "border-none"}`}>
          {isOpen && (
            // Div with user logged in 
            <div>
              <p className="text-sm text-gray-400">Logged in as:</p>
              <p className="text-sm font-bold">ondra.faltin@gmail.com</p>
            </div>
          )}
        
          {/* Button to toggle the sidebar (open/close it) */}
          <button onClick={toggleSidebar} className="p-2 bg-transparent border-none cursor-pointer focus:outline-none">
            <img
              src="/img/sidebar.svg"
              alt="Toggle Sidebar"
              className="h-6 w-6"
            />
          </button>
        </SidebarFooter>

      </Sidebar>
    </div>
  );
}