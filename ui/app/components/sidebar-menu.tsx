"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation"; 
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarHeader,
} from "@/app/components/sidebar";
import { Button } from "@/app/components/button";

export function SidebarMenu() {
  const [isOpen, setIsOpen] = useState(true); 
  const router = useRouter(); 

  const toggleSidebar = () => setIsOpen(!isOpen);

  const handleLogout = () => {
    setTimeout(() => {
        router.push("/"); // Redirect to homepage
    }, 0);
  };

  return (
    <div className={`flex ${isOpen ? "w-[14%]" : "w-[4%]"} transition-all`}>
      <Sidebar
        className={`bg-[#09090B] text-white h-screen flex flex-col ${
          isOpen ? "border-e border-[#27272A]" : "border-none"
        }`}
      >
        {/* Sidebar Header */}
        <SidebarHeader
          className={`p-4 ${
            isOpen ? "border-b border-[#27272A]" : "border-none"
          }`}
        >
          {isOpen && <img src="/img/Text-white.png" alt="JečnáBot Logo" />}
        </SidebarHeader>

        {/* Sidebar Content */}
        <SidebarContent className="flex-1 p-4 space-y-6 relative">
          {isOpen && (
            <>
              {/* Logout Button */}
              <div className="absolute bottom-0 left-0 w-full p-4">
                <Button
                  className="w-full bg-red-500 hover:bg-red-600 text-white"
                  onClick={handleLogout}
                >
                  Logout
                </Button>
              </div>
            </>
          )}
        </SidebarContent>

        {/* Sidebar Footer */}
        <SidebarFooter
          className={`p-4 flex items-center justify-between ${
            isOpen ? "border-t border-[#27272A]" : "border-none"
          }`}
        >
          {isOpen && (
            <div>
              <p className="text-sm text-gray-400">Logged in as:</p>
              <p className="text-sm font-bold">Ondřej Faltin</p>
            </div>
          )}
          <button
            onClick={toggleSidebar}
            className="p-2 bg-transparent border-none cursor-pointer focus:outline-none"
          >
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