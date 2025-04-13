import React, { useState } from 'react';

interface InputSelectorProps {
    label: string;
    options: string[];
    value?: string;
    onChange?: (value: any) => void;
    className?: string
}

const InputSelector: React.FC<InputSelectorProps> = ({ label, options, value = "", onChange, className }) => {
    const [selectedValue, setSelectedValue] = useState(value);

    const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        const newValue = event.target.value;
        setSelectedValue(newValue);
        if (onChange) {
            onChange(newValue);
        }
    };

    return (
        <div className="relative w-full">
            <select
                className={`
                peer w-full border border-gray-600 dark:border-gray-50 rounded
                focus:outline-none focus:ring-2 focus:ring-blue-500
                placeholder-transparent transition-all duration-300 ease-in-out
                disabled:bg-gray-400 dark:disabled:bg-gray-600 dark:bg-gray-800 dark:text-white ${className}
                `}
                value={selectedValue}
                onChange={handleChange}
                data-cy={"input-selector"}
            >
                <option value="" disabled>
                    Select an option
                </option>
                {options.map((option) => (
                    <option
                        key={option}
                        value={option}
                        data-cy={`theme-option-${option}`}
                    >
                        {option}
                    </option>
                ))}
            </select>
        </div>
    );
};

export default InputSelector;
