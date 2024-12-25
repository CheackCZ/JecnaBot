"use client";

import React, { useState, useEffect, useRef } from "react";
import { Input } from "@/app/components/input";
import { Button } from "@/app/components/button";
import { SidebarMenu } from "@/app/components/sidebar-menu";

type Message = {
  id: number;
  sender: "user" | "bot";
  text: string;
};

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const websocket = useRef<WebSocket | null>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to the bottom whenever messages are updated
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  useEffect(() => {
    websocket.current = new WebSocket("ws://localhost:7777");
    websocket.current.onopen = () => {
      console.log("Connected to WebSocket server");
    };
    websocket.current!.onmessage = (event) => {
      const response: string = event.data;
      setMessages((prevMessages) => [
        ...prevMessages,
        { id: Date.now(), sender: "bot", text: response },
      ]);
    };
    websocket.current.onclose = () => {
      console.log("WebSocket connection closed");
    };
    websocket.current.onerror = (error) => {
      console.error("WebSocket error", error);
    };

    return () => {
      websocket.current?.close();
    };
  }, []);

  const handleSend = () => {
    if (input.trim() === "") return;

    const newMessage: Message = { id: Date.now(), sender: "user", text: input };
    setMessages((prevMessages) => [...prevMessages, newMessage]);
    websocket.current?.send(input);
    setInput("");
  };

  return (
    <div className="flex h-screen bg-[#09090B]">
      <SidebarMenu />
      <main className="flex-1 flex flex-col">
        <header className="w-[60%] mx-[20%] flex justify-center p-4 border-b border-[#27272A]">
          <img className="h-[50px]" src="/img/Text-white.png" alt="sidebar" />
        </header>

        <div
          ref={chatContainerRef}
          className="flex-1 mx-[20%] w-[60%] items-center p-4 overflow-y-auto bg-[#09090B] custom-scroll"
        >
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex mb-4 ${
                message.sender === "user" ? "justify-end" : "justify-start"
              }`}
            >
              {message.sender === "bot" && (
                <img
                  src="/img/Logo.png"
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
                {message.sender === "bot" ? (
                  <pre className="whitespace-pre-wrap">{message.text}</pre>
                ) : (
                  message.text
                )}
              </div>
            </div>
          ))}
        </div>

        <div className="p-4 mx-[20%] w-[60%] bg-[#09090B] flex items-center space-x-4">
          <Input
            type="text"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="flex-1 bg-black text-white placeholder-gray-500 px-4 py-2 rounded-md border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            style={{ backgroundColor: "#09090B" }}
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
