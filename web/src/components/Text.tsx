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
    const sizeClasses = {
        xs: "text-xs",
        sm: "text-sm",
        base: "text-base",
        lg: "text-lg",
        xl: "text-xl",
        "2xl": "text-2xl",
        "3xl": "text-3xl",
        "4xl": "text-4xl",
        "5xl": "text-5xl",
        "6xl": "text-6xl"
    };

    const weightClasses = {
        thin: "font-thin",
        extralight: "font-extralight",
        light: "font-light",
        normal: "font-normal",
        medium: "font-medium",
        semibold: "font-semibold",
        bold: "font-bold",
        extrabold: "font-extrabold",
        black: "font-black"
    };

    return (
        <span className={`${sizeClasses[size]} ${weightClasses[weight]} ${className || ''}`}>
            {children}
        </span>
    );
};

export default Text;
