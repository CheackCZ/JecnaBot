import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Combines class names conditionally and merges Tailwind utility classes.
 * @param inputs - Array of class names or conditions.
 * @returns A single string of merged class names.
 */
export function cn(...inputs: string[]) {
  return twMerge(clsx(inputs));
}