
"use client"; // Indicates this component is client-side rendered in Next.js.

import React, { useState } from "react"; // Import React and useState for state management.
import { useRouter } from "next/navigation"; // Import useRouter for programmatic navigation in Next.js.
import { Input } from "@/app/components/input"; // Import reusable Input component.
import { Button } from "@/app/components/button"; // Import reusable Button component.

export default function Register() {
  const router = useRouter(); // Create a router instance for navigation.

  // States for managing email and password input fields.
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // Function to handle the registration form submission.
  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault(); // Prevent default form submission behavior.

    // Mock registration logic (replace with actual API call).
    alert("Registration successful!");
    router.push("/login"); 
};

  return (
    // Main div 
    <div className="flex flex-row items-center justify-center min-h-screen bg-[#09090B]">
      
      {/* Entire Logo of the Application */}
      <div className="w-[50%] h-screen flex items-center justify-center ps-[10%] bg-white">
        <img src="/img/Full-Logo.png" alt="" />
      </div>

      {/* Div with form for user credentials input */}
      <div className="w-[50%] h-screen flex flex-col items-center justify-center pe-[10%]">
        {/* Form title */}
        <h1 className="text-3xl font-semibold text-center mt-6 mb-6">Create an Account!</h1>
        
        {/* Form */}
        <form onSubmit={handleRegister} className="space-y-4 w-[60%]">

          {/* Div with Email details */}
          <div>
            {/* Email Label */}
            <label htmlFor="email" className="block text-sm font-medium mb-1">
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

          {/* Div with Password details. */}
          <div>
            {/* Password Label */}
            <label htmlFor="password" className="block text-sm font-medium mb-1">
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

          {/* Div with Password details. */}
          <div>
            {/* Password Label */}
            <label htmlFor="password" className="block text-sm font-medium mb-1">
              Repeat Password
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

          {/* Div with TextArea (for reason to be able to use the bot) */}
          <div className="grid w-full gap-1.5">
            <label htmlFor="message">Why should we allow you to use our AI model?</label>
            <textarea className="w-full text-white bg-[#09090B] border border-[#27272A] placeholder-[#27272A] hover:border-white focus:border-white focus:ring focus:ring-[#09090B] rounded" placeholder="Type here." id="message" />
          </div>

          {/* Registration Button */}
          <Button type="submit" className="w-full bg-white text-[#09090B] font-bold">Register</Button>
        </form>
      
      </div>

    </div>
  );
}