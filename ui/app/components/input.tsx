import * as React from "react"; // Import React for creating components and managing refs.

// Define the interface for InputProps, extending standard HTML input attributes.
export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {}

// Create the Input component using React's forwardRef for ref forwarding.
const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, ...props }, ref) => {
    return (

      <input
        ref={ref} 
        className={`flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:opacity-50 disabled:cursor-not-allowed ${className}`} 
        {...props} 
      />

    );
  }
);

// Set a display name for the Input component.
Input.displayName = "Input";

export { Input };