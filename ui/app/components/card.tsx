import * as React from "react"; // Import React for creating components and managing refs.

// Define the interface for CardProps, which extends standard HTML div attributes.
export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {}

// Create the Card component using React's forwardRef for ref forwarding.
const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, children, ...props }, ref) => {
    return (
      
      <div ref={ref} className={`rounded-lg border border-gray-300 bg-white p-4 shadow-md ${className}`}  {...props}>
        {children}
      </div>
    
  );
  }
);

// Set a display name for the Card component.
Card.displayName = "Card";

export { Card };