import React, { useRef } from 'react';
import { useNavigate } from "react-router-dom";

import { IconButtonProps } from "@/components/IconButton";

interface ButtonProps extends IconButtonProps {
    variant?: 'primary' | 'secondary' | 'success' | 'danger';
    size?: 'small' | 'medium' | 'large';
    to?: string;
    disabled?: boolean;
}

const Button: React.FC<ButtonProps> = ({
    variant = 'primary',
    size = 'medium',
    onClick = undefined,
    to = "",
    disabled = false,
    className = "",
    children,
    ...props
}) => {
    const navigate = useNavigate();
    const buttonRef = useRef<HTMLButtonElement>(null);
    const clickEffectRef = useRef<HTMLSpanElement>(null);

    const baseClasses = '' +
        'font-bold rounded shadow transition duration-300 text-center relative ' +
        'ease-in-out focus:outline-none focus:ring-2 ' +
        'focus:ring-opacity-50 overflow-hidden';

    const getButtonClasses = () => {
        let classes = baseClasses;

        if (!disabled) {

            switch (variant) {
                case 'primary':
                    classes += ' bg-blue-500 hover:bg-blue-600 text-white';
                    break;
                case 'secondary':
                    classes += ' bg-gray-500 hover:bg-gray-600 text-white';
                    break;
                case 'success':
                    classes += ' bg-green-500 hover:bg-green-600 text-white';
                    break;
                case 'danger':
                    classes += ' bg-red-500 hover:bg-red-600 text-white';
                    break;
            }
        }
        else {
            classes += ' bg-gray-300 text-gray-500 cursor-not-allowed';
        }

        switch (size) {
            case 'small':
                classes += ' px-3 py-1 text-sm';
                break;
            case 'medium':
                classes += ' px-4 py-2 text-base';
                break;
            case 'large':
                classes += ' px-6 py-3 text-lg';
                break;
        }
        return classes;
    };

    const handleClick = async (e: React.MouseEvent<HTMLButtonElement>) => {
        if (disabled) {
            e.preventDefault();
            return;
        }
        const button: HTMLButtonElement | null = buttonRef.current;
        const clickEffect: HTMLSpanElement | null = clickEffectRef.current;

        if (button && clickEffect) {
            const buttonRect = button.getBoundingClientRect();
            const { left, top } = buttonRect;
            const leftOffset = e.clientX - left;
            const topOffset = e.clientY - top;

            clickEffect.style.left = `${leftOffset}px`;
            clickEffect.style.top = `${topOffset}px`;

            clickEffect.classList.add('animate-click-effect');

            setTimeout(() => {
                clickEffect.classList.remove('animate-click-effect');
            }, 600);

            if (to) navigate(to, { replace: true });
            if (onClick) await onClick();
        }
    }

    return (
        <button ref={buttonRef} className={`${getButtonClasses()} ${className}`} onClick={handleClick} {...props}>
            {children}
            <span ref={clickEffectRef} className={"w-10 h-10 absolute rounded-4xl"}></span>
        </button>
    );
};

export default Button;
