"use client";

import React, { useState, useEffect, useRef } from "react";
import { Input } from "@/app/components/input";
import { Button } from "@/app/components/button";
import { SidebarMenu } from "@/app/components/sidebar-menu";

// Define the type for messages used in the chat
type Message = {
  id: number;          
  sender: "user" | "bot"; 
  text: string;        
};

export default function Chat() {
  // State to manage the list of chat messages
  const [messages, setMessages] = useState<Message[]>([]);
  // State to manage the input field value
  const [input, setInput] = useState("");
  // State to store a list of frequently asked questions (FAQs)
  const [questions, setQuestions] = useState<{ id: number; text: string }[]>([]);
  // State to handle typing effect for bot responses
  const [currentTypingMessage, setCurrentTypingMessage] = useState<string>("");
  // Reference to the WebSocket connection
  const websocket = useRef<WebSocket | null>(null);
  // Reference to the chat container for scrolling
  const chatContainerRef = useRef<HTMLDivElement>(null);

  // Effect to auto-scroll the chat container when messages update
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages, currentTypingMessage]);

  // Effect to establish a WebSocket connection when the component mounts
  useEffect(() => {
    const token = localStorage.getItem("token"); 

    if (!token) {
      console.error("No token found. Redirecting to login.");
      window.location.href = "/login"; 
      return;
    }

    // Initialize WebSocket connection
    websocket.current = new WebSocket(`ws://localhost:7777?token=${token}`);

    // Handle WebSocket connection open
    websocket.current.onopen = () => {
      console.log("WebSocket connection opened");
    };

    // Handle incoming messages from the WebSocket server
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
          startTypingEffect(data.message);
        }
      } catch (err) {
        console.error("Error parsing WebSocket message:", err);
      }
    };

    // Handle WebSocket connection close
    websocket.current.onclose = () => {
      console.log("WebSocket connection closed");
    };

    // Handle WebSocket errors
    websocket.current.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    // Clean up WebSocket connection on component unmount
    return () => {
      console.log("Cleaning up WebSocket connection...");
      websocket.current?.close();
    };
  }, []);

  // Function to handle typing effect for bot responses
  const startTypingEffect = (message: string) => {
    const words = message.split(" ");
    let index = 0;
    setCurrentTypingMessage(""); 

    // Simulate typing effect by appending words incrementally
    const typingInterval = setInterval(() => {
      setCurrentTypingMessage((prev) => `${prev} ${words[index]}`.trim());
      index++;

      if (index === words.length) {
        clearInterval(typingInterval);
        setMessages((prev) => [
          ...prev,
          { id: Date.now(), sender: "bot", text: message },
        ]);
        setCurrentTypingMessage("");
      }
    }, 100); 
  };

  // Function to handle sending a message
  const handleSend = () => {
    if (input.trim() === "") return;

    // Create a new user message
    const newMessage: Message = { id: Date.now(), sender: "user", text: input };
    setMessages((prevMessages) => [...prevMessages, newMessage]);

    websocket.current?.send(input); 

    setInput(""); 
    setQuestions([]); 
  };

  // Function to handle question button clicks
  const handleQuestionClick = (questionId: number, questionText: string) => {
    websocket.current?.send(questionId.toString()); 

    // Add the question as a user message
    const newMessage: Message = { id: Date.now(), sender: "user", text: questionText };
    setMessages((prevMessages) => [...prevMessages, newMessage]);

    setQuestions([]); 
  };

  // Handle Enter key press for sending messages
  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleSend();
    }
  };

  return (

    <div className="flex h-screen bg-[#09090B]">
      {/* SidebarMenu Component */}
      <SidebarMenu />
    
      <main className="flex-1 flex flex-col">

        {/* Header section */}
        <header className="w-[60%] mx-[20%] flex justify-center p-4 border-b border-[#27272A]">
          <img className="h-[50px]" src="/img/Text-white.png" alt="sidebar" />
        </header>

        {/* Chat container */}
        <div ref={chatContainerRef} className="flex-1 mx-[20%] w-[60%] p-4 overflow-y-auto bg-[#09090B] custom-scroll">
          {messages.map((message) => (
            <div key={message.id} className={`flex mb-4 ${message.sender === "user" ? "justify-end" : "justify-start"}`}>
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
                {message.text}
              </div>
            </div>
          ))}

          {/* Typing effect */}
          {currentTypingMessage && (
            <div className="flex mb-4 justify-start">
              <img
                src="/img/Logo.png"
                alt="Bot"
                className="h-10 w-10 mr-2 rounded-full border border-[#27272A]"
              />
              <div className="inline-block px-4 py-2 bg-[#09090B] border border-[#27272A] text-white rounded-lg">
                {currentTypingMessage}
              </div>
            </div>
          )}

          {/* Render Frequently Asked Questions as Buttons */}
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

        {/* Input section */}
        <div className="p-4 mx-[20%] w-[60%] bg-[#09090B] flex items-center space-x-4">
          <Input
            type="text"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
            className="flex-1 bg-black text-white placeholder-gray-500 px-4 py-2 rounded-md border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            style={{ backgroundColor: "#09090B" }}
          />
          <Button onClick={handleSend} className="bg-blue-500 hover:bg-blue-600 text-white">Send</Button>
        </div>
        
      </main>
    </div>
  );
}