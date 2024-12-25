"use client";

import React, { useState } from "react";
import { Input } from "@/app/components/input";
import { Button } from "@/app/components/button";
import { SidebarMenu } from "@/app/components/sidebar-menu";

export default function Chat() {

  // State for storing chat messages.
  const [messages, setMessages] = useState([
    { id: 1, sender: "bot", text: "Hi! How can I help you?" },
  ]);

  // State for the current user input in the chat input field.
  const [input, setInput] = useState("");

  // Function to handle sending messages.
  const handleSend = () => {
    // Prevent sending empty messages.
    if (input.trim() === "") return;

    // Create a new message object with a unique ID, the user as the sender, and the current input as the text.
    const newMessage = { id: Date.now(), sender: "user", text: input };
    
    setMessages([...messages, newMessage]);
    setInput("");
  };

  return (
    // Main div
    <div className="flex h-screen bg-[#09090B]">
      {/* Sidebar(Menu) */}
      <SidebarMenu />

      {/* Chat Window */}
      <main className="flex-1 flex flex-col">
        
        {/* Chat Header */}
        <header className="w-[60%] mx-[20%] flex justify-center p-4 border-b border-[#27272A]">
          {/* Logo */}
          <img className="h-[50px]" src="/img/Text-white.png" alt="sidebar" />
        </header>

        {/* Messages */}
        <div className="flex-1 mx-[20%] w-[60%] items-center p-4 overflow-y-auto bg-[#09090B]">
          
          {messages.map((message) => (
            
            <div key={message.id} className={`flex mb-4 ${ message.sender === "user" ? "justify-end" : "justify-start"}`}>

              {/* Bot Messages */}
              {message.sender === "bot" && (
                <img
                  src="/img/Logo.png" 
                  alt="Bot"
                  className="h-10 w-10 mr-2 rounded-full border border-[#27272A]"
                />
              )}

              {/* User Messages */}
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

        {/* Message Input Div */}
        <div className="p-4 mx-[20%] w-[60%] bg-[#09090B] flex items-center space-x-4">
          
          {/* Input */}
          <Input
            type="text"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="flex-1 bg-black text-white placeholder-gray-500 px-4 py-2 rounded-md border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            style={{backgroundColor : "#09090B"}}
          />
          
          {/* Send Button */}
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