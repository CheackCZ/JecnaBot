"use client";

import React, { useState } from "react";
import { useUserContext } from "@/hooks/UserContext";
import { useRouter } from "next/navigation";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarHeader,
} from "@/app/components/sidebar";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/app/components/alert-dialog";
import { useToast } from "@/hooks/use-toast";
import { Toaster } from "@/app/components/toaster";

export function SidebarMenu({ onToggle }: { onToggle: (isOpen: boolean) => void }) {
  const [isOpen, setIsOpen] = useState(true);
  const router = useRouter();
  const { toast } = useToast();

  const { email } = useUserContext(); 

  const toggleSidebar = () => {
    const newState = !isOpen;
    setIsOpen(newState);
    onToggle(newState); 
  };

  const handleLogout = () => {
    document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
    router.push("/login");
  };
  
  const chatHistory = [
    { id: 1, title: "Support Chat", date: "Dec 28, 2024" },
    { id: 2, title: "Order Inquiry", date: "Dec 27, 2024" },
    { id: 3, title: "Feedback Session", date: "Dec 25, 2024" },
  ];

  const handleChatHistoryClick = (chatId: number, chatTitle: string) => {
    toast({
      title: "Coming soon...",
      description: `The history of chats will be implemented soon. (Chat ID: ${chatId}, Title: ${chatTitle})`,
    });
  };

  return (
    <div
    className={`xs:fixed xs:top-0 xs:left-0 xs:z-50 sm:static ${
      isOpen ? "lg:w-[320px] md:w-[240px] sm:w-[200px] xs:w-full" : "w-[40px]"
    } h-screen transition-all`}
  >
    {/* Sidebar */}
    {isOpen && (
      <Sidebar
        className={`bg-[#09090B] text-white h-full flex flex-col ${
          isOpen ? "border-e border-[#27272A]" : "border-none"
        }`}
      >
        {/* Sidebar Header */}
        <SidebarHeader className="p-4 flex items-center justify-between border-b border-[#27272A]">
          <div className="overflow-hidden">
            <p className="text-sm text-gray-400 truncate">Logged in as:</p>
            <p className="text-sm font-bold truncate">{email}</p>
          </div>
          <button
            onClick={toggleSidebar}
            className="p-2 border-none cursor-pointer focus:outline-none"
          >
            <img src="/img/sidebar.svg" alt="Toggle Sidebar" className="h-6 w-6" />
          </button>
        </SidebarHeader>

        {/* Sidebar Content */}
        <SidebarContent className="flex-1 p-4 space-y-6 overflow-y-auto">
          <SidebarGroup>
            <h2 className="text-sm font-semibold text-gray-500 mb-4 truncate">Chat History</h2>
            <ul className="mt-2 space-y-3 custom-sidebar-scroll">
              {chatHistory.map((chat) => (
                <li
                  key={chat.id}
                  className="flex items-center p-3 bg-[#1A1A1A] hover:bg-[#27272A] rounded-lg cursor-pointer"
                  onClick={() => handleChatHistoryClick(chat.id, chat.title)}
                >
                  <img src="/img/Chat.svg" alt="Chat Icon" className="h-5 w-5 mr-3" />
                  <div className="truncate">
                    <p className="text-sm font-medium truncate">{chat.title}</p>
                    <p className="text-xs text-gray-400 truncate">{chat.date}</p>
                  </div>
                </li>
              ))}
            </ul>
          </SidebarGroup>
        </SidebarContent>

        {/* Sidebar Footer */}
        <SidebarFooter className="p-4 border-t border-[#27272A]">
          <AlertDialog>
            <AlertDialogTrigger asChild>
              <button className="w-full px-4 py-2 text-white bg-red-500 rounded hover:bg-red-600">
                Logout
              </button>
            </AlertDialogTrigger>
            <AlertDialogContent>
              <AlertDialogHeader>
                <AlertDialogTitle>Confirm Logout</AlertDialogTitle>
                <AlertDialogDescription>
                  Are you sure you want to log out? This action cannot be undone.
                </AlertDialogDescription>
              </AlertDialogHeader>
              <AlertDialogFooter>
                <AlertDialogCancel>Cancel</AlertDialogCancel>
                <AlertDialogAction onClick={handleLogout} className="bg-red border-none">
                  Logout
                </AlertDialogAction>
              </AlertDialogFooter>
            </AlertDialogContent>
          </AlertDialog>
        </SidebarFooter>
      </Sidebar>
    )}

    {/* Toggle Button (Visible when Sidebar is hidden) */}
    {!isOpen && (
      <button
        onClick={toggleSidebar}
        className="fixed top-[20px] left-4 p-2 border-none cursor-pointer z-50"
      >
        <img src="/img/sidebar.svg" alt="Open Sidebar" className="h-6 w-6" />
      </button>
    )}

    <Toaster />
  </div>
  );
}