import React from "react";

import { ChatInterface } from "../interfaces/instances/chat";




function Conversation() {
    const messages = [
        {role: "user", text: "How can I make sure the menu stays within the viewport?"},
        {
            role: "ai",
            text: "This component ensures the menu stays within the viewport when opened. This version dynamically adjusts the menu's position if it would overflow the left or right edges of the screen."
        },
    ];

    return (
        <div className="flex flex-col items-center justify-center w-full h-screen">
            <div
                className="flex flex-col w-full max-w-3xl h-[100vh] overflow-y-auto"
                style={{ scrollBehavior: 'smooth' }}
            >
                <div className="pb-36">
                    {messages.map((msg, index) => (
                        <div
                            key={index}
                            className={`${msg.role === "ai" ? "w-full" : "max-w-[75%] ml-auto"}`}
                        >
                            {msg.role === "user" ? (
                                <div className="ml-auto px-2 py-3">
                                    <div className="flex justify-end">
                                        <div className="p-4 bg-gray-200 dark:bg-gray-800 rounded-lg">
                                            {msg.text}
                                        </div>
                                    </div>
                                </div>
                            ) : (
                                <div className="px-6 py-6">
                                    <div className="flex flex-col">
                                        <div className="w-8 h-8 rounded-sm flex items-center justify-center bg-blue-500 text-white mb-2">
                                            AI
                                        </div>
                                        <div className="text-base leading-relaxed">
                                            {msg.text}
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default Conversation;
