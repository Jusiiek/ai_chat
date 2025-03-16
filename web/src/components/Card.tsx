import React from "react";

interface CardProps {
  children: React.ReactNode;
  onClick?: () => void;
  className?: string;
  style?: React.CSSProperties;
}

const Card: React.FC<CardProps> = ({ children, onClick, className, style }) => {
  return (
    <div
        className={
          `rounded-lg shadow-lg overflow-hidden bg-gray-200 dark:bg-gray-800 p-10 ${className} ${onClick ? 'cursor-pointer' : ''}`
        }
        style={style}
        onClick={onClick}
    >
      { children }
    </div>
  );
};

export default Card;
