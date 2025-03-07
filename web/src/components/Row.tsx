import React from "react";

interface RowProps {
  className?: string;
  children?: React.ReactNode;
}

const Row: React.FC<RowProps> = ({ className, children }) => {
    return (
        <div className={`flex flex-row ${className}`}>
            { children }
        </div>
    )
}

export default Row;