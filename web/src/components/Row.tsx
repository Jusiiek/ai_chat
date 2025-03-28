import React from "react";

export interface RowProps {
  className?: string;
  children?: React.ReactNode;
  style?: React.CSSProperties;
}

const Row: React.FC<RowProps> = ({ className, style, children }) => {
    return (
        <div className={`flex flex-row ${className}`} style={style}>
            { children }
        </div>
    )
}

export default Row;