"use client"; // Indicates this component is client-side rendered in Next.js.

import React, { useState } from "react"; // Import React and useState for state management.
import { useRouter } from "next/navigation"; // Import useRouter for programmatic navigation in Next.js.
import { Input } from "@/app/components/input"; // Import reusable Input component.
import { Button } from "@/app/components/button"; // Import reusable Button component.

export default function Register() {
  const router = useRouter(); // Create a router instance for navigation.

  // States for managing email, password, and repeat-password input fields.
  const [email, setEmail] = useState(""); // State for email input.
  const [password, setPassword] = useState(""); // State for password input.
  const [repeatPassword, setRepeatPassword] = useState(""); // State for repeat password input.
  const [error, setError] = useState(""); // State to handle error messages.

  // Function to validate password strength (matches backend validation logic).
  const isValidPassword = (password:string) => {
    const passwordRegex =
      /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$/;
    return passwordRegex.test(password);
  };

  // Function to handle the registration form submission.
  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault(); // Prevent default form submission behavior.

    // Check if passwords match
    if (password !== repeatPassword) {
      setError("Passwords do not match. Please try again."); // Display error if passwords don't match.
      return;
    }

    // Check if password is valid
    if (!isValidPassword(password)) {
      setError(
        "Password must have at least 1 number, 1 special character, 1 uppercase letter, 1 lowercase letter, and be at least 8 characters long."
      );
      return;
    }

    setError(""); // Clear any previous error messages.

    try {
      // Send registration data to the server.
      const response = await fetch("http://localhost:5000/register", {
        method: "POST", // Use POST method for sending data.
        headers: {
          "Content-Type": "application/json", // Indicate JSON content type.
        },
        body: JSON.stringify({
          username: email, // Send email as username.
          password: password, // Send password.
        }),
      });

      if (response.ok) {
        alert("Registration successful!"); // Notify user of successful registration.
        router.push("/login"); // Redirect to the login page.
      } else {
        const errorData = await response.json(); // Parse error response from the server.
        setError(errorData.error || "Registration failed."); // Display server-provided error.
      }
    } catch (error) {
      console.error("Error registering user:", error); // Log error for debugging.
      setError("An error occurred. Please try again."); // Notify user of an error.
    }
  };

  return (
    // Main container for the registration page.
    <div className="flex md:flex-row xs:flex-col items-center justify-center min-h-screen bg-[#09090B]">
      {/* Left side: Logo display */}
      <div className="md:w-[50%] sm:w-[360px] xs:w-[240px] md:h-screen sm:h-[40vh] xs:h-[35vh] flex items-center justify-center md:ps-[10%] md:bg-white">
        <img src="/img/Full-Logo.png" alt="Full Logo" className="hidden md:block" />
        <img src="/img/Full-logo-white.png" alt="Full Logo (white)" className="block md:hidden" />
      </div>

      {/* Right side: Registration form */}
      <div className="md:w-[50%] xs:w-[100%] md:h-screen sm:h-[60vh] xs:h-[65vh] flex flex-col items-center md:justify-center xs:justify-start md:pe-[10%]">
        {/* Form title */}
        <h1 className="md:text-3xl sm:text-2xl xs:text-xl text-white font-semibold text-center md:mt-6 mb-6 space-y-4 w-[60%]">
          Create an Account!
        </h1>

        {/* Form element */}
        <form onSubmit={handleRegister} className="space-y-4 md:w-[60%] xs:w-[60%]">
          {/* Email input field */}
          <div>
            {/* Email label */}
            <label htmlFor="email" className="block text-sm text-gray-100 font-medium mb-1">
              Email
            </label>
            {/* Email input */}
            <Input
              id="email"
              type="email"
              placeholder="Enter your email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)} // Update email state on input change.
              className="w-full text-[#09090B] bg-[#09090B] border border-[#27272A] placeholder-[#27272A] hover:border-white focus:border-white focus:ring focus:ring-[#09090B]"
            />
          </div>

          {/* Password input field */}
          <div>
            {/* Password label */}
            <label htmlFor="password" className="block text-sm text-gray-100 font-medium mb-1">
              Password
            </label>
            {/* Password input */}
            <Input
              id="password"
              type="password"
              placeholder="Enter your password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)} // Update password state on input change.
              className="w-full text-[#09090B] bg-[#09090B] border border-[#27272A] placeholder-[#27272A] hover:border-white focus:border-white focus:ring focus:ring-[#09090B]"
            />
          </div>

          {/* Repeat password input field */}
          <div>
            {/* Repeat Password label */}
            <label
              htmlFor="repeat-password"
              className="block text-sm text-gray-100 font-medium mb-1"
            >
              Repeat Password
            </label>
            {/* Repeat Password input */}
            <Input
              id="repeat-password"
              type="password"
              placeholder="Repeat your password"
              required
              value={repeatPassword}
              onChange={(e) => setRepeatPassword(e.target.value)} // Update repeat password state on input change.
              className="w-full text-[#09090B] bg-[#09090B] border border-[#27272A] placeholder-[#27272A] hover:border-white focus:border-white focus:ring focus:ring-[#09090B]"
            />
          </div>

          {/* Error message display */}
          {error && <p className="text-red-500 text-sm mt-2">{error}</p>}

          {/* Registration button */}
          <Button
            type="submit"
            className="w-full bg-blue-500 text-[#09090B] font-bold"
          >
            Register
          </Button>
        </form>

        {/* Link to the login page */}
        <div className="mt-4 text-center space-y-4 w-[60%]">
          <p className="text-gray-500 break-words">
            Already have an account?{" "}
            <span
              className="text-blue-500 cursor-pointer hover:underline"
              onClick={() => router.push("/login")}
            >
              Login
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