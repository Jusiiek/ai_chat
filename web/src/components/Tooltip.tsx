import React, { useState, useRef } from "react";

interface TooltipProps {
    content: string;
    children: React.ReactNode;
    placement?: "top" | "bottom" | "left" | "right";
}

const Tooltip: React.FC<TooltipProps> = ({content, children, placement = "bottom"}) => {
    const [visible, setVisible] = useState(true);
    const tooltipRef = useRef<HTMLDivElement>(null);

    const handleMouseEnter = () => {
        setVisible(true);
    };

    const handleMouseLeave = () => {
        setVisible(false);
    };

    const getTooltipStyles = () => {
        switch (placement) {
            case "top":
                return {bottom: "100%", left: "50%", transform: "translateX(-50%)", marginBottom: "8px"};
            case "left":
                return {right: "100%", top: "50%", transform: "translateY(-50%)", marginRight: "8px"};
            case "right":
                return {left: "100%", top: "50%", transform: "translateY(-50%)", marginLeft: "8px"};
            default:
                return {top: "100%", left: "50%", transform: "translateX(-50%)", marginTop: "8px"};
        }
    };

    const getArrowStyles = () => {
        switch (placement) {
            case "top":
                return {bottom: "-6px", left: "50%", transform: "translateX(-50%) rotate(45deg)"};
            case "left":
                return {right: "-6px", top: "50%", transform: "translateY(-50%) rotate(45deg)"};
            case "right":
                return {left: "-6px", top: "50%", transform: "translateY(-50%) rotate(45deg)"};
            default:
                return {top: "-6px", left: "50%", transform: "translateX(-50%) rotate(45deg)"};
        }
    };

    return (
        <div className="relative inline-block" onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
            {children}
            {visible && (
                <div
                    ref={tooltipRef}
                    className="absolute z-10 p-3 text-white bg-black rounded shadow-lg w-48 max-w-[160px] text-center"
                    style={getTooltipStyles()}
                >
                    <div
                        className="absolute w-3 h-3 bg-black transform"
                        style={getArrowStyles()}
                    />
                    {content}
                </div>
            )}
        </div>
    );
};

export default Tooltip;