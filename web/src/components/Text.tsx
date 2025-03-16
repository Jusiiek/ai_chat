import React from "react";

interface TextProps {
  children: React.ReactNode;
  size?: "xs" | "sm" | "base" | "lg" | "xl" | "2xl" | "3xl" | "4xl" | "5xl" | "6xl";
  weight?: "thin" | "extralight" | "light" | "normal" | "medium" | "semibold" | "bold" | "extrabold" | "black";
  className?: string;
}

const Text: React.FC<TextProps> = ({
    children,
    size = "base",
    weight = "normal",
    className,
}) => {
    return (
        <span className={`text-${size} font-${weight} ${className}`}
        >
            {children}
        </span>
    );
};

export default Text;
