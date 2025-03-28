import React, { useState } from "react";

export interface IconButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    children: React.ReactNode;
    onClick?: () => void | Promise<void>;
    className?: string;
}

const IconButton: React.FC<IconButtonProps> = ({children, onClick, className = ""}) => {
    const [isClicked, setIsClicked] = useState(false);

    const handleClick = () => {
        setIsClicked(true);
        setTimeout(() => setIsClicked(false), 150);
        if (onClick) onClick();
    };

    return (
        <button
            onClick={handleClick}
            className={`flex items-center justify-center rounded transition-transform duration-150 ease-out ${isClicked ? "scale-90" : "scale-100"} ${className}`}
        >
            {children}
        </button>
    );
};

export default IconButton;