// Navbar.tsx
import React from "react";
import { useDispatch, useSelector } from "react-redux";


import { setSidebarState } from "../reducers/siderbar";

import {
    Row,
    Col,
    ThemeSwitcher,
    Avatar,
    Tooltip,
    IconButton
} from "../components";
import {RootState} from "@/store";

interface NavbarProps {
    className?: string
}

const Navbar: React.FC<NavbarProps> = ({className}) => {
    const dispatch = useDispatch();

    const openSidebar = () => {
        dispatch(setSidebarState(true));
    }
    const isSidebarOpen = useSelector((state: RootState) => state.sidebar.isOpen);
    return (
        <Row className={`w-full h-full bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-600 py-[18px] px-[12px] ${className}`}>
            <Col className={"justify-center items-start w-1/2"}>
                <Row className={"items-center"}>
                    {
                        !isSidebarOpen ?
                            <div>
                                <Tooltip content={"Open sidebar"} placement={"right"}>
                                    <IconButton onClick={openSidebar}>
                                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                                             viewBox="0 0 24 24" fill="none"
                                             stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                             stroke-linejoin="round"
                                             className="lucide lucide-table-2">
                                            <path
                                                d="M9 3H5a2 2 0 0 0-2 2v4m6-6h10a2 2 0 0 1 2 2v4M9 3v18m0 0h10a2 2 0 0 0 2-2V9M9 21H5a2 2 0 0 1-2-2V9m0 0h18"/>
                                        </svg>
                                    </IconButton>
                                </Tooltip>
                            </div> :
                            ''
                    }

                    {
                        !isSidebarOpen ?
                            <div className={"mr-3 ml-3"}>
                                <Tooltip content={"New Chat"} placement={"right"}>
                                    <IconButton>
                                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                                             viewBox="0 0 24 24" fill="none"
                                             stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                             stroke-linejoin="round"
                                             className="lucide lucide-square-pen">
                                            <path d="M12 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                                            <path
                                                d="M18.375 2.625a1 1 0 0 1 3 3l-9.013 9.014a2 2 0 0 1-.853.505l-2.873.84a.5.5 0 0 1-.62-.62l.84-2.873a2 2 0 0 1 .506-.852z"/>
                                        </svg>
                                    </IconButton>
                                </Tooltip>
                            </div> :
                            ""
                    }
                    <div>MODEL_NAME</div>
                </Row>
            </Col>
            <Col className={"justify-center items-end w-1/2"}>
                <Row className={"items-center"}>
                    <ThemeSwitcher className={"mr-3"}/>
                    <Avatar/>
                </Row>
            </Col>
        </Row>
    );
};

export default Navbar;
