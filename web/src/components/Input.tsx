import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
    label: string;
    type?: React.HTMLInputTypeAttribute;
}

const Input: React.FC<InputProps> = ({ label, type = "text", onChange, value, name, ...props }) => {
    return (
        <div className="relative w-full">
            <input
                type={type}
                className="peer w-full px-4 pt-5 pb-2 border border-gray-600 dark:border-gray-50 rounded
                focus:outline-none focus:ring-2 focus:ring-blue-500
                placeholder-transparent transition-all duration-300 ease-in-out
                disabled:bg-gray-400 dark:disabled:bg-gray-600 dark:text-gray-900"
                id={props.id}
                name={name}
                placeholder=" "
                onChange={onChange}
                value={value}
                {...props}
            />

            <label
                className={`absolute left-4 top-4 text-gray-500 dark:text-gray-300 px-1
                transition-all duration-300 ease-in-out transform
                bg-white dark:bg-gray-900
                peer-placeholder-shown:top-4 peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-400 peer-placeholder-shown:bg-transparent
                peer-focus:-top-2 peer-focus:text-sm peer-focus:text-blue-500 peer-focus:scale-90 peer-focus:bg-white peer-focus:dark:bg-gray-900
                peer-[&:not(:placeholder-shown)]:-top-2 peer-[&:not(:placeholder-shown)]:text-sm peer-[&:not(:placeholder-shown)]:text-blue-500 peer-[&:not(:placeholder-shown)]:scale-90 peer-[&:not(:placeholder-shown)]:bg-white peer-[&:not(:placeholder-shown)]:dark:bg-gray-900`}
                htmlFor={props.id}
            >
                {label}
            </label>
        </div>
    );
};



export default Input;
