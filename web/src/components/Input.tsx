import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
    label: string;
}

const Input: React.FC<InputProps> = ({label, ...props}) => {
    return (
        <div className="flex flex-col">
            <label className="font-bold mb-2" htmlFor={props.id}>{label}</label>
            <input
                className="px-4 py-2 border border-gray-600 dark:border-gray-50 rounded
                focus:outline-none focus:ring-2 focus:ring-blue-500"
                {...props}
            />
        </div>
    )
}

export default Input;
