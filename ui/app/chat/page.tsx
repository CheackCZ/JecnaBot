"use client";

import React, { useState, useEffect, useRef } from "react";
import { Input } from "@/app/components/input";
import { Button } from "@/app/components/button";
import { SidebarMenu } from "@/app/components/sidebar-menu";
import { useUserContext } from "@/hooks/UserContext";

// Define the type for messages used in the chat
type Message = {
  id: number;
  sender: "user" | "bot";
  text: string;
  loading?: boolean; 
};

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);

  const [input, setInput] = useState("");
  
  const [isWaitingForResponse, setIsWaitingForResponse] = useState(false);
  
  const [questions, setQuestions] = useState<{ id: number; text: string }[]>([]);
  
  const websocket = useRef<WebSocket | null>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  const { email } = useUserContext();

  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  const handleSidebarToggle = (isOpen: boolean) => {
    setIsSidebarOpen(isOpen);
  };

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      console.error("No token found. Redirecting to login.");
      window.location.href = "/login";
      return;
    }

    websocket.current = new WebSocket(`ws://localhost:7777?token=${token}`);

    websocket.current.onopen = () => {
      console.log("WebSocket connection opened");
    };

    websocket.current.onmessage = (event) => {
      console.log("WebSocket message received:", event.data);
      try {
        const data = JSON.parse(event.data);

        if (data.type === "welcome") {
          setMessages((prev) => [
            ...prev,
            { id: Date.now(), sender: "bot", text: data.message },
          ]);
          setQuestions(data.questions || []);
        } else if (data.type === "response" || data.type === "info") {
          handleBotResponse(data.message);
        }
      } catch (err) {
        console.error("Error parsing WebSocket message:", err);
      } finally {
        setIsWaitingForResponse(false); 
      }
    };

    websocket.current.onclose = () => {
      console.log("WebSocket connection closed");
    };

    websocket.current.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    return () => {
      console.log("Cleaning up WebSocket connection...");
      websocket.current?.close();
    };
  }, []);

  const handleBotResponse = (message: string) => {
    const loadingMessageId = Date.now();
    setMessages((prev) => [
      ...prev,
      { id: loadingMessageId, sender: "bot", text: "...", loading: true },
    ]);

    setTimeout(() => {
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === loadingMessageId
            ? { ...msg, text: message, loading: false }
            : msg
        )
      );
    }, 1000); // Simulate a delay
  };

  const handleSend = () => {
    if (input.trim() === "") return;

    const newMessage: Message = { id: Date.now(), sender: "user", text: input };
    setMessages((prevMessages) => [...prevMessages, newMessage]);

    setIsWaitingForResponse(true);
    websocket.current?.send(input);

    setInput("");
    setQuestions([]);
  };

  const handleQuestionClick = (questionId: number, questionText: string) => {
    websocket.current?.send(questionId.toString());

    const newMessage: Message = { id: Date.now(), sender: "user", text: questionText };
    setMessages((prevMessages) => [...prevMessages, newMessage]);

    setQuestions([]);
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !isWaitingForResponse) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex h-screen w-full bg-[#09090B]">
      <SidebarMenu onToggle={handleSidebarToggle}/>

      <main className="flex-1 flex flex-col">
        <header className="lg:w-[60%] sm:w-[80%] xs:w-[100%] lg:mx-[20%] sm:mx-[10%] xs:mx-0 flex justify-center p-4 border-b border-[#27272A]">
          <img className="h-[50px]" src="/img/Text-white.png" alt="sidebar" />
        </header>

        <div ref={chatContainerRef} className="flex-1 lg:w-[60%] sm:w-[80%] xs:w-[100%] lg:mx-[20%] sm:mx-[10%] xs:mx-0 p-4 overflow-y-auto bg-[#09090B] custom-scroll">
        {messages.map((message) => (
            <div
            key={message.id}
            className={`flex mb-4 ${message.sender === "user" ? "justify-end" : "justify-start"}`}
          >
            {/* Show bot image for both loading and regular bot messages */}
            {message.sender === "bot" && (
              <img
                src="/img/Logo.png"
                alt="Bot"
                className={`h-10 w-10 mr-2 rounded-full border border-[#27272A]`}
              />
            )}
            <div
              className={`inline-block max-w-[80%] px-4 py-2 rounded-lg ${
                message.loading
                  ? "bg-transparent text-gray-500 animate-pulse"
                  : message.sender === "user"
                  ? "bg-white text-[#09090B]"
                  : "bg-[#09090B] border border-[#27272A] text-white"
              }`}
            >
              {message.text}
            </div>
          </div>
          ))}

          {questions.length > 0 && (
            <div className="mt-4">
              <p className="text-white mb-2">Frequently Asked Questions:</p>
              <div className="flex flex-wrap gap-2">
                {questions.map((question) => (
                  <button
                    key={question.id}
                    onClick={() => handleQuestionClick(question.id, question.text)}
                    className="bg-[#09090B] border border-[#27272A] hover:bg-white text-white hover:text-[#09090B] px-4 py-2 rounded-lg"
                  >
                    {question.text}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="p-4 lg:w-[60%] sm:w-[80%] xs:w-[90%] lg:mx-[20%] sm:mx-[10%] xs:mx-[5%] bg-[#09090B] flex items-center space-x-4">
          <Input
            type="text"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
            className="flex-1 bg-black text-white placeholder-gray-500 px-4 py-2 rounded-md border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            style={{ backgroundColor: "#09090B" }}
          />
          <Button
            onClick={handleSend}
            disabled={isWaitingForResponse}
            className={`bg-blue-500 hover:bg-blue-600 text-white ${
              isWaitingForResponse ? "opacity-50 cursor-not-allowed" : ""
            }`} 
          >
            Send
          </Button>
        </div>

      </main>
    </div>
  );
}