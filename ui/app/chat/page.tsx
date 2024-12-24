"use client";

import React, { useState } from "react";
import { Input } from "@/app/components/input";
import { Button } from "@/app/components/button";
import { SidebarMenu } from "@/app/components/sidebar-menu";

export default function Chat() {
  const [messages, setMessages] = useState([
    { id: 1, sender: "bot", text: "Hi! How can I help you?" },
  ]);
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (input.trim() === "") return;

    const newMessage = { id: Date.now(), sender: "user", text: input };
    setMessages([...messages, newMessage]);
    setInput("");
  };

  return (
    <div className="flex h-screen bg-[#09090B]">
      {/* Sidebar */}
      <SidebarMenu />

      {/* Chat Window */}
      <main className="flex-1 flex flex-col">
        {/* Chat Header */}
        <header className="w-[60%] mx-[20%] flex justify-center p-4 border-b border-[#27272A]">
          <img className="h-[50px]" src="/img/Text-white.png" alt="sidebar" />
        </header>

        {/* Messages */}
        <div className="flex-1 mx-[20%] w-[60%] items-center p-4 overflow-y-auto bg-[#09090B]">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex mb-4 ${
                message.sender === "user" ? "justify-end" : "justify-start"
              }`}
            >
              {message.sender === "bot" && (
                <img
                  src="/img/Logo.png" // Replace with your bot icon image path
                  alt="Bot"
                  className="h-10 w-10 mr-2 rounded-full border border-[#27272A]"
                />
              )}
              <div
                className={`inline-block px-4 py-2 rounded-lg ${
                  message.sender === "user"
                    ? "bg-white text-[#09090B]"
                    : "bg-[#09090B] border border-[#27272A] text-white"
                }`}
              >
                {message.text}
              </div>
            </div>
          ))}
        </div>

        {/* Message Input */}
        <div className="p-4 mx-[20%] w-[60%] bg-[#09090B] flex items-center space-x-4">
          <Input
            type="text"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="flex-1 bg-black text-white placeholder-gray-500 px-4 py-2 rounded-md border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            style={{backgroundColor : "#09090B"}}
          />
          <Button
            onClick={handleSend}
            className="bg-blue-500 hover:bg-blue-600 text-white"
          >
            Send
          </Button>
        </div>
      </main>
    </div>
  );
}
