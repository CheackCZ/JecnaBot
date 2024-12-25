import * as React from "react"; // Import React for creating components.
import { VariantProps, cva } from "class-variance-authority"; // Import `cva` for managing CSS variants and `VariantProps` for type inference.
import { cn } from "@/lib/utils"; // Import a utility function `cn` for merging class names dynamically.

// Define buttonVariants using `cva` for styling and managing CSS classes dynamically.
const buttonVariants = cva(
  // Base styles for the button, shared across all variants and sizes.
  "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-background",
  {
    variants: {
      // Define the `variant` property for different button styles.
      variant: {
        default: "bg-blue-500 text-white hover:bg-blue-600",
        outline: "border border-gray-300 text-gray-700 hover:bg-gray-100",
        ghost: "bg-transparent hover:bg-gray-100",
      },
      // Define the `size` property for button dimensions.
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-8 px-3",
        lg: "h-12 px-6",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

// Define the ButtonProps interface, extending HTML button attributes and `VariantProps` for type-safe variant support.
export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

// Create a React Button component using `forwardRef` for ref forwarding.
const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => {
    return (

      <button
        ref={ref}
        className={cn(buttonVariants({ variant, size }), String(className))}
        {...props}
      />
    
    );
  }
);

// Set the display name for the Button component.
Button.displayName = "Button";

export { Button, buttonVariants };