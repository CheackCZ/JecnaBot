"use client"; // Indicates this component is client-side rendered in Next.js.

import React, { useState } from "react"; // Import React and useState for state management.
import { useRouter } from "next/navigation"; // Import useRouter for programmatic navigation in Next.js.
import { Input } from "@/app/components/input"; // Import reusable Input component.
import { Button } from "@/app/components/button"; // Import reusable Button component.
import { Alert, AlertDescription, AlertTitle } from "@/app/components/alert"

export default function Login() {
  const router = useRouter(); // Create a router instance for navigation.

  // States for managing email and password input fields.
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // Function to handle login form submission.
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await fetch("http://localhost:5000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: email,
          password: password,
        }),
      });

      if (response.ok) {
        const data = await response.json();

        alert("Login successful!");
        
        localStorage.setItem("token", data.token); // Save the session token
        router.push("/chat");
      } else {
        const errorData = await response.json();

        alert(errorData.error || "Login failed.");
      }
    } catch (error) {
      console.error("Error logging in:", error);
      
      alert("An error occurred. Please try again.");
    }
  };

  return (
    // Main container for the login page.
    <div className="flex flex-row items-center justify-center min-h-screen bg-[#09090B]">
      {/* Left side: Logo display */}
      <div className="w-[50%] h-screen flex items-center justify-center ps-[10%] bg-white">
        <img src="/img/Full-Logo.png" alt="" /> {/* Full logo of the application */}
      </div>

      {/* Right side: Login form */}
      <div className="w-[50%] h-screen flex flex-col items-center justify-center pe-[10%]">
        {/* Form title */}
        <h1 className="text-3xl text-white font-semibold text-center mt-6 mb-6">Welcome back!</h1>

        {/* Form element */}
        <form onSubmit={handleLogin} className="space-y-4 w-[60%]">
          {/* Email input field */}
          <div>
            {/* Email Label */}
            <label htmlFor="email" className="block text-sm text-gray-100 font-medium mb-1">
              Email
            </label>

            {/* Email Input */}
            <Input
              id="email"
              type="email"
              placeholder="Enter your email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full text-[#09090B] bg-[#09090B] border border-[#27272A] placeholder-[#27272A] hover:border-white focus:border-white focus:ring focus:ring-[#09090B]"
            />
          </div>

          {/* Password input field */}
          <div>
            {/* Password Label */}
            <label htmlFor="password" className="block text-sm text-gray-100 font-medium mb-1">
              Password
            </label>

            {/* Password Input */}
            <Input
              id="password"
              type="password"
              placeholder="Enter your password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full text-[#09090B] bg-[#09090B] border border-[#27272A] placeholder-[#27272A] hover:border-white focus:border-white focus:ring focus:ring-[#09090B]"
            />
          </div>

          {/* Login button */}
          <Button
            type="submit"
            className="w-full bg-white text-[#09090B] font-bold"
          >
            Login
          </Button>
        </form>

        {/* Link to the registration page */}
        <div className="mt-4 text-center">
          <p className="text-gray-500">
            Don't have an account already?{" "}
            <span
              className="text-blue-500 cursor-pointer hover:underline"
              onClick={() => router.push("/register")}
            >
              Register
            </span>
          </p>
        </div>
      </div>
    </div>
  );
}