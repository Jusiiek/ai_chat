import React, {useState, useRef, useEffect} from "react";

type DropdownProps = {
    children: React.ReactNode;
};

type TriggerProps = {
    children: React.ReactNode;
};

type MenuProps = {
    children: React.ReactNode;
    className?: string;
};

type MenuItemProps = {
    children: React.ReactNode;
    onClick?: () => void | Promise<void>;
    className?: string;
    disabled?: boolean;
};

const DropdownContext = React.createContext<{
    isOpen: boolean;
    setIsOpen: React.Dispatch<React.SetStateAction<boolean>>;
}>({
    isOpen: false,
    setIsOpen: () => {
    },
});

const Dropdown = ({children}: DropdownProps) => {
    const [isOpen, setIsOpen] = useState(false);
    const dropdownRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const handleClickOutside = (e: MouseEvent) => {
            if (
                dropdownRef.current &&
                !dropdownRef.current.contains(e.target as Node)
            ) {
                setIsOpen(false);
            }
        };

        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    return (
        <DropdownContext.Provider value={{isOpen, setIsOpen}}>
            <div ref={dropdownRef} className="relative inline-block">
                {children}
            </div>
        </DropdownContext.Provider>
    );
};

const Trigger = ({children}: TriggerProps) => {
    const {setIsOpen} = React.useContext(DropdownContext);

    return React.cloneElement(children as React.ReactElement, {
        onClick: () => setIsOpen((prev) => !prev),
    });
};

const Menu = ({children, className = ""}: MenuProps) => {
    const {isOpen} = React.useContext(DropdownContext);
    const menuRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (menuRef.current && isOpen) {
            const menuRect = menuRef.current.getBoundingClientRect();
            const viewportWidth = window.innerWidth;
            let leftPosition = 0;

            if (menuRect.right > viewportWidth) {
                leftPosition = viewportWidth - menuRect.width - menuRect.left;
            } else if (menuRect.left < 0) {
                leftPosition = -menuRect.left;
            }

            menuRef.current.style.transform = `translateX(${leftPosition}px)`;
        }
    }, [isOpen]);

    return isOpen ? (
        <div
            ref={menuRef}
            className={`absolute z-50 mt-1 min-w-[120px] rounded-md bg-white dark:bg-black shadow-lg ring-1 ring-black ring-opacity-5 ${className}`}
        >
            <ul>
                {children}
            </ul>
        </div>
    ) : null;
};

const MenuItem = ({children, onClick, className = "", disabled}: MenuItemProps) => {
    const {setIsOpen} = React.useContext(DropdownContext);

    const handleClick = () => {
        if (disabled) return;
        onClick?.();
        setIsOpen(false);
    };

    return (
        <div
            onClick={handleClick}
            className={
                `px-4 py-2 text-sm cursor-pointer hover:bg-gray-100 hover:dark:bg-neutral-900 ${disabled ? "opacity-50 cursor-not-allowed" : ""} ${className}`
            }
        >
            {children}
        </div>
    );
};

Dropdown.Trigger = Trigger;
Dropdown.Menu = Menu;
Dropdown.MenuItem = MenuItem;

export default Dropdown;
