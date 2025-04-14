import React from "react";

import {MessageInterface} from "../interfaces/instances/message";

interface ConversationInterface {
    messages?: MessageInterface[] | undefined
}


function Conversation({messages}: ConversationInterface) {
    return (
        <div className="flex flex-col items-center justify-center w-full h-screen">
            <div
                className="flex flex-col w-full max-w-3xl h-[100vh] overflow-y-auto"
                style={{scrollBehavior: 'smooth'}}
            >
                <div className="pb-36">
                    {
                        messages && messages?.length ?
                            messages.map((msg, index) => (
                                <div
                                    key={index}
                                    className={`${msg.author_role === "ai" ? "w-full" : "max-w-[75%] ml-auto"}`}
                                >
                                    {msg.author_role === "user" ? (
                                        <div className="ml-auto px-2 py-3">
                                            <div className="flex justify-end">
                                                <div className="p-4 bg-gray-200 dark:bg-gray-800 rounded-lg">
                                                    {msg.content}
                                                </div>
                                            </div>
                                        </div>
                                    ) : (
                                            msg.author_role === "ai" && msg.isLoading ? (
                                                <div className="px-6 py-6">
                                                    <div className="flex flex-col text-left">
                                                        <div
                                                            className="w-8 h-8 rounded-sm flex items-center justify-center bg-blue-500 text-white mb-2"
                                                        >
                                                            AI
                                                        </div>
                                                        <div className="text-base leading-relaxed flex items-center">
                                                            <span className="loading-dots">
                                                                <span>.</span>
                                                                <span>.</span>
                                                                <span>.</span>
                                                              </span>
                                                        </div>
                                                    </div>
                                                </div>
                                            ) : (
                                                <div className="px-6 py-6">
                                                    <div className="flex flex-col text-left">
                                                        <div
                                                            className="w-8 h-8 rounded-sm flex items-center justify-center bg-blue-500 text-white mb-2"
                                                        >
                                                            AI
                                                        </div>
                                                        <div className="text-base leading-relaxed">
                                                            {msg.content}
                                                        </div>
                                                    </div>
                                                </div>
                                            )
                                        )
                                    }
                                </div>
                            )) : ''
                    }
                </div>
            </div>
        </div>
    );
}

export default Conversation;
