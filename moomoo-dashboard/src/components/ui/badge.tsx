import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const badgeVariants = cva(
  "inline-flex items-center rounded-full border px-3 py-1 text-xs font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
  {
    variants: {
      variant: {
        default: "border-transparent bg-moo-yellow text-gray-900",
        secondary: "border-transparent bg-gray-100 text-gray-700",
        success: "border-transparent bg-green-50 text-green-700 border-green-200",
        warning: "border-transparent bg-yellow-50 text-yellow-700 border-yellow-200",
        error: "border-transparent bg-red-50 text-red-700 border-red-200",
        outline: "border-gray-200 text-gray-600 bg-white hover:bg-gray-50",
        climate: "border-transparent bg-moo-green/10 text-moo-green border-moo-green/20",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props} />
  );
}

export { Badge, badgeVariants };
