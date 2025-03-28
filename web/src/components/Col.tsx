import React from "react";

import { RowProps } from "./Row"

const Col: React.FC<RowProps> = ({ className, style, children }) => {
    return (
        <div className={`flex flex-col ${className}`} style={style}>
            { children }
        </div>
    )
}

export default Col;