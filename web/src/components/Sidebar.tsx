import React, {useEffect, useState} from 'react';
import {useDispatch, useSelector} from "react-redux";
import {useParams, useNavigate} from "react-router-dom";

import {setSidebarState} from "../reducers/siderbar";
import {ThreadsService} from "../services/thread";
import {CategorizedThreads} from "../interfaces/instances/thread";
import { PATHS } from "../router/routes";

import {
    Row,
    Col,
    Tooltip,
    IconButton,
    Icon,
    Text
} from "../components";
import {RootState} from "@/store";


const Sidebar: React.FC = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const isSidebarOpen = useSelector((state: RootState) => state.sidebar.isOpen);

    const {thread_id} = useParams();
    const [threadId, setThreadId] = useState<string | null>(null);
    const [threadList, setThreadList] = useState<CategorizedThreads>({});

    useEffect(() => {
        // Prevents state updates if component unmounts
        let isMounted = true;

        const watchThread = async () => {
            if (!isMounted) return;
            await new Promise(resolve => setTimeout(resolve, 500));

            if (isMounted) {
                setThreadId(thread_id || null);
                if (thread_id) {
                    const {data} = await ThreadsService.getThreadList();
                    setThreadList(data)
                }
            }
        };

        watchThread();

        return () => {
            isMounted = false;
        };
    }, [thread_id]);

    useEffect(() => {
        const fetchThreads = async () => {
            try {
                const {data} = await ThreadsService.getThreadList();
                setThreadList(data);
            } catch (error) {
                console.error("Error fetching thread list:", error);
            }
        };
        fetchThreads();

        return () => {
        };
    }, []);

    const closeSidebar = () => {
        dispatch(setSidebarState(false));
    }

    const createNewChat = () => {
        closeSidebar();
        navigate(PATHS.HOME, { replace: true });
    }

    return (
        <nav
            className={`d-flex w-full h-full bg-gray-800 text-white ${isSidebarOpen ? '' : 'overflow-hidden'}`}
        >
            <Row className={`w-full py-[23px] px-[12px]`}>
                <Col className={"justify-start items-start align-middle w-1/2"}>
                    <div className="flex justify-center items-center">
                        <Tooltip content={"Close sidebar"} placement={"right"}>
                            <IconButton onClick={closeSidebar}>
                                <Icon name={"table"}/>
                            </IconButton>
                        </Tooltip>
                    </div>
                </Col>
                <Col className={"justify-start items-end align-middle w-1/2"}>
                    <div className="flex justify-center items-center">
                        <Tooltip content={"New Chat"} placement={"right"}>
                            <IconButton onClick={createNewChat}>
                                <Icon name={"square-pen"}/>
                            </IconButton>
                        </Tooltip>
                    </div>
                </Col>
            </Row>
            <Col className="w-full gap-2 mt-5 last:mb-5">
                {Object.entries(threadList).map(([category, threads]) => (
                    <Col className="w-full mb-2" key={category}>
                        <Row className="py-2 px-[12px]">
                            <Text size={"xs"} weight={"bold"}>
                                {category}
                            </Text>
                        </Row>
                        <Col className="space-y-2">
                            <ol>
                                {threads.map((thread) => (
                                    <li
                                        key={thread.id}
                                        className={`py-2 px-[12px] rounded-xl ${threadId === thread.id ? 'bg-gray-200 dark:bg-gray-600' : ''}`}
                                    >
                                        <IconButton className={"w-full items-start"}>
                                            <Text size={"base"} weight={"light"}>
                                                {thread.title}
                                            </Text>
                                        </IconButton>
                                    </li>
                                ))}
                            </ol>
                        </Col>
                    </Col>
                ))}
            </Col>
        </nav>
    )
}

export default Sidebar;
