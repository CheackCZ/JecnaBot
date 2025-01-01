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
} from "@/app/components/alert-dialog"; // Adjust import path as per your setup
import { useToast } from "@/hooks/use-toast"; // Hook for toast notifications
import { Toaster } from "@/app/components/toaster";

export function SidebarMenu() {
  const [isOpen, setIsOpen] = useState(true);
  const router = useRouter();
  const { toast } = useToast();

  const toggleSidebar = () => setIsOpen(!isOpen);

  const handleLogout = () => {
    router.push("/"); // Redirect to the homepage
  };

  // Mock chat history data
  const chatHistory = [
    { id: 1, title: "Support Chat", date: "Dec 28, 2024" },
    { id: 2, title: "Order Inquiry", date: "Dec 27, 2024" },
    { id: 3, title: "Feedback Session", date: "Dec 25, 2024" },
  ];

  // Handle chat history item click
  const handleChatHistoryClick = (chatId: number, chatTitle: string) => {
    toast({
      title: "Coming soon...",
      description: `The history of chats will be implemented soon. (Chat ID: ${chatId}, Title: ${chatTitle})`,
    });
  };

  return (
    <div className={`flex ${isOpen ? "w-[14%]" : "w-[4%]"} transition-all`}>
      <Sidebar
        className={`bg-[#09090B] text-white h-screen flex flex-col ${
          isOpen ? "border-e border-[#27272A]" : "border-none"
        }`}
      >
        {/* Sidebar Header with User Info and Toggle Button */}
        <SidebarHeader
          className={`p-4 flex items-center justify-between gap-x-8 ${
            isOpen ? "border-b border-[#27272A]" : "border-none"
          }`}
        >
          {isOpen && (
            <div>
              <p className="text-sm text-gray-400">Logged in as:</p>
              <p className="text-sm font-bold">ondra.faltin@gmail.com</p>
            </div>
          )}
          <button
            onClick={toggleSidebar}
            className="p-2 bg-transparent border-none cursor-pointer focus:outline-none"
          >
            <img src="/img/sidebar.svg" alt="Toggle Sidebar" className="h-6 w-6" />
          </button>
        </SidebarHeader>

        {/* Sidebar Content */}
        <SidebarContent className="flex-1 p-4 space-y-6">
          {isOpen && (
            <SidebarGroup>
              <h2 className="text-sm font-semibold text-gray-500 mb-4">Chat History</h2>
              <ul className="mt-2 space-y-3 custom-sidebar-scroll overflow-y-auto">
                {chatHistory.map((chat) => (
                  <li
                    key={chat.id}
                    className="flex items-center p-3 bg-[#1A1A1A] hover:bg-[#27272A] rounded-lg cursor-pointer"
                    onClick={() => handleChatHistoryClick(chat.id, chat.title)} // Show toast on click
                  >
                    <img
                      src="/img/Chat.svg"
                      alt="Chat Icon"
                      className="h-5 w-5 mr-3"
                    />
                    <div>
                      <p className="text-sm font-medium">{chat.title}</p>
                      <p className="text-xs text-gray-400">{chat.date}</p>
                    </div>
                  </li>
                ))}
              </ul>
            </SidebarGroup>
          )}
        </SidebarContent>

        {/* Sidebar Footer with Logout Dialog */}
        {isOpen && (
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
                  <AlertDialogCancel>
                    Cancel
                  </AlertDialogCancel>
                  <AlertDialogAction onClick={handleLogout} className="bg-red border-none">
                    Logout
                  </AlertDialogAction>
                </AlertDialogFooter>
              </AlertDialogContent>
            </AlertDialog>
          </SidebarFooter>
        )}
      </Sidebar>

      {/* Toaster for displaying notifications */}
      <Toaster />
    </div>
  );
}