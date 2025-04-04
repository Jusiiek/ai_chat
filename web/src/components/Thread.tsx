import React, {useState, useEffect} from "react";
import {useParams, useNavigate} from "react-router-dom";

import {
    Row,
    Conversation,
    IconButton,
    Icon
} from "../components";
import {useSelector} from "react-redux";

import {ThreadsService} from "../services/thread";
import {ChatsService} from "../services/chat";
import {Task} from "../services/task";
import {RootState} from "../store";
import {ThreadInterface} from "../interfaces/instances/thread";
import {MessageInterface} from "@/interfaces/instances/message";

function Thread() {
    const navigate = useNavigate();

    const isSidebarOpen = useSelector((state: RootState) => state.sidebar.isOpen);
    const [message, setMessage] = useState("hi");

    const {thread_id} = useParams();
    const [threadId, setThreadId] = useState<string | null>(null);
    const [thread, setThread] = useState<Partial<ThreadInterface>>({})
    const [conversation, setConversation] = useState<Partial<MessageInterface[]>>([])
    const [chatId, setChatId] = useState<string>("")

    useEffect(() => {
        // Prevents state updates if component unmounts
        let isMounted = true;

        const watchThread = async () => {
            if (!isMounted) return;
            await new Promise(resolve => setTimeout(resolve, 500));

            if (isMounted) {
                setThreadId(thread_id || null);
                if (thread_id) {
                    const {data} = await ThreadsService.getThread(thread_id);
                    setThread(data);
                    for (let i = 0; i < data.conversations.length; i++) {
                        console.log(data.conversations[i].messages)
                        setConversation((prevMessages) => [
                            ...prevMessages,
                            ...data.conversations[i].messages
                        ]);
                    }

                }
            }
        };

        watchThread();

        return () => {
            isMounted = false;
        };
    }, [thread_id]);

    const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        const {value} = e.target;
        setMessage(value);
    };

    const createChat = async () => {
        if (threadId) {
            const tempMessage: MessageInterface = {
                id: `temp-${Date.now()}`,
                chat_id: threadId,
                author_role: "user",
                content: message,
                created_at: new Date(),
                updated_at: new Date(),
            };

            setConversation((prev) => [...prev, tempMessage]);
            const {res, data} = await ChatsService.createChat(threadId, message);
            if (res.status === 200) {
                const task = new Task(data)

                task.onSuccess = (result) => {
                    console.log('Task succeeded:', result);
                    setChatId(result)
                };

                task.onFailure = (error) => {
                    console.error('Task failed:', error);
                };
                task.start();
            }
        } else {
            const {res, data} = await ThreadsService.createThread(message);
            if (res.status === 200) {
                const task = new Task(data)

                task.onSuccess = (result) => {
                    console.log('Task succeeded:', result);
                    navigate(`/${result}`);
                };

                task.onFailure = (error) => {
                    console.error('Task failed:', error);
                };
                task.start();
            }
        }
    }

    useEffect(() => {
        const fetchData = async () => {
            if (chatId) {
                try {
                    const {data} = await ChatsService.getChat(chatId);
                    setConversation((prev) => [
                        ...prev.filter((msg) => msg?.id && !msg.id.startsWith("temp-")),
                        ...data.messages,
                    ]);
                } catch (error) {
                    console.error("Error fetching data:", error);
                }
            }
        };

        fetchData();
    }, [chatId]);

    return (
        <Row className={"flex-1 grow basis-auto flex-col"}>
            <div
                className={"h-full overflow-y-scroll"}
            >
                <Conversation messages={conversation.filter((msg): msg is MessageInterface => msg !== undefined)}/>
            </div>
            <div
                className={`fixed bottom-0 transition-all duration-300 ease-in-out ${isSidebarOpen ? 'left-[300px] right-0' : 'left-0 right-0'}`}>
                <div className="max-w-3xl mx-auto p-4">
                    <div className="relative">
                        <textarea
                            className="w-full p-3 pr-12 rounded-lg border border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white resize-none"
                            placeholder="Type a message..."
                            onChange={handleInputChange}
                            value={message}
                            rows={1}
                        />
                        <IconButton className="absolute right-3 top-3 text-blue-500 hover:text-blue-600"
                                    onClick={createChat}>
                            <Icon name="triangular-arrow"/>
                        </IconButton>
                    </div>
                </div>
            </div>
        </Row>
    )
}

export default Thread;
