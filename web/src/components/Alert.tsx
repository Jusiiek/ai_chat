import React, {useEffect} from "react";
import {useDispatch, useSelector} from "react-redux";
import {RootState} from "../store";
import {resetAlert} from "../reducers/alert";

const Alert = () => {
    const dispatch = useDispatch();
    const alertState = useSelector((state: RootState) => state.alert);

    useEffect(() => {
        let timer: NodeJS.Timeout;
        if (alertState.show) {
            timer = setTimeout(() => {
                dispatch(resetAlert());
                }, 5000);
        }
        return () => {
            if (timer) clearTimeout(timer);
        };
    }, [alertState.show, dispatch]);

    if (!alertState.show) return null;

    const getBorderColor = () => {
        switch (alertState.color) {
            case 'success':
                return 'border-green-500 dark:border-green-300';
            case 'danger':
                return 'border-red-500 dark:border-red-300';
            case 'info':
                return 'border-blue-500 dark:border-blue-300';
            default:
                return 'border-gray-300 dark:border-gray-500';
        }
    };

    const getTextColor = () => {
        switch (alertState.color) {
            case 'success':
                return 'text-green-700 dark:text-green-100';
            case 'danger':
                return 'text-red-700 dark:text-red-100';
            case 'info':
                return 'text-blue-700 dark:text-blue-100';
            default:
                return 'text-green-700 dark:text-green-100';
        }
    };

    return (
        <div
            className={`
                fixed top-0 left-1/2 -translate-x-1/2 w-full max-w-4xl z-[9999] p-4
                border rounded-lg shadow-lg bg-white dark:bg-gray-800
                ${getBorderColor()} transition-all duration-300
            `}
        >
            <div className={`flex items-center justify-between ${getTextColor()}`}>
                <span className="flex-1 text-center">{alertState.content}</span>
                <button
                    onClick={() => dispatch(resetAlert())}
                    className="ml-4 text-xl font-bold hover:opacity-75"
                >
                    &times;
                </button>
            </div>
        </div>
    );
};

export default Alert;
