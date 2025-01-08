"use client"; // Indicates this component is client-side rendered in Next.js.

import React, { useState } from "react"; // Import React and useState for state management.
import { useRouter } from "next/navigation"; // Import useRouter for programmatic navigation in Next.js.
import { Input } from "@/app/components/input"; // Import reusable Input component.
import { Button } from "@/app/components/button"; // Import reusable Button component.
import { Alert, AlertDescription, AlertTitle } from "@/app/components/alert"
import { useUserContext } from "@/hooks/UserContext";


export default function Login() {
  const router = useRouter();
  const { setEmail } = useUserContext(); // Access setEmail from context
  const [email, setEmailInput] = useState("");
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
        alert("Login successfull.");
        const data = await response.json();

        document.cookie = `token=${data.token}; path=/; secure; samesite=strict;`;

        setEmail(email); // Set email in context
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
    <div className="flex md:flex-row xs:flex-col items-center justify-center min-h-screen bg-[#09090B]">
      {/* Left side: Logo display */}
      <div className="md:w-[50%] sm:w-[360px] xs:w-[240px] md:h-screen sm:h-[40vh] xs:h-[35vh] flex items-center justify-center md:ps-[10%] md:bg-white">
        <img src="/img/Full-Logo.png" alt="Full Logo" className="hidden md:block" />
        <img src="/img/Full-logo-white.png" alt="Full Logo (white)" className="block md:hidden" />
      </div>

      {/* Right side: Login form */}
      <div className="md:w-[50%] xs:w-[100%] md:h-screen sm:h-[60vh] xs:h-[65vh] flex flex-col items-center md:justify-center xs:justify-start md:pe-[10%]">
        {/* Form title */}
        <h1 className="md:text-3xl sm:text-2xl xs:text-xl text-white font-semibold text-center md:mt-6 mb-6 space-y-4 w-[60%]">
          Welcome Back!
        </h1>

        {/* Form element */}
        <form onSubmit={handleLogin} className="space-y-4 md:w-[60%] xs:w-[60%]">
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
              onChange={(e) => setEmailInput(e.target.value)}
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
            className="w-full bg-blue-500 text-[#09090B] font-bold"
          >
            Login
          </Button>
        </form>

        {/* Link to the registration page */}
        <div className="mt-4 text-center space-y-4 w-[60%]">
          <p className="text-gray-500 break-words">
            Don't have an account already?{" "}
            <span
              className="text-blue-500 cursor-pointer hover:underline"
              onClick={() => router.push("/register")}
            >
              Register
            </span>
          </p>

          {/* Div with link to home */}
          <div className="mt-2">
            <a href="/" className="text-gray-500 break-words">
              Return to <span className="text-blue-500 cursor-pointer hover:underline">Home Page</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}