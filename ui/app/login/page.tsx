"use client"

import React from "react";
import { useRouter } from "next/navigation";

import { Input } from "@/app/components/input";
import { Button } from "@/app/components/button";

export default function Login() {
  const router = useRouter();

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();

    console.log("Logging in...");
    router.push("/chat");   
  };

  return (
    <div className="flex flex-row items-center justify-center min-h-screen bg-[#09090B]">
      
      <div className="w-[50%] h-screen flex items-center justify-center ps-[10%] bg-white">
        <img src="/img/Full-Logo.png" alt="" />
      </div>

      <div className="w-[50%] h-screen flex flex-col items-center justify-center pe-[10%]">
        <h1 className="text-3xl font-semibold text-center mt-6 mb-6">Welcome back!</h1>

        <form onSubmit={handleLogin} className="space-y-4 w-[60%]">
          <div>
            <label htmlFor="email" className="block text-sm font-medium mb-1">
              Email
            </label>
            <Input
              id="email"
              type="email"
              placeholder="Enter your email"
              required
              className="w-full text-[#09090B] bg-[#09090B] border border-[#27272A] placeholder-[#27272A] hover:border-white focus:border-white focus:ring focus:ring-[#09090B]"
            />
          </div>
          <div>
            <label htmlFor="password" className="block text-sm font-medium mb-1">
              Password
            </label>
            <Input
              id="password"
              type="password"
              placeholder="Enter your password"
              required
              className="w-full text-[#09090B] bg-[#09090B] border border-[#27272A] placeholder-[#27272A] hover:border-white focus:border-white focus:ring focus:ring-[#09090B]"
            />
          </div>
          <Button type="submit" className="w-full bg-white text-[#09090B] font-bold">
            Login
          </Button>
        </form>
        <p className="text-sm text-center text-gray-600 mt-4">
          Don’t have an account?{" "}
          <a href="/register" className="text-blue-500 hover:underline">
            Register
          </a>
        </p>
      </div>

        
    </div>
  );
}
