import React from 'react';
import { useDispatch } from "react-redux";

import { setSidebarState } from "../reducers/siderbar";

import { Row, Col, Tooltip, IconButton } from "../components";


const Sidebar: React.FC = () => {
    const dispatch = useDispatch();

    const closeSidebar = () => {
        dispatch(setSidebarState(false));
    }

    return (
        <Row className={"w-100 bg-black overflow-hidden"}>
            <Row className={`w-full py-[23px] px-[12px]`}>
                <Col className={"justify-center items-start align-middle w-1/2"}>
                    <div className="flex justify-center items-center">
                        <Tooltip content={"Close sidebar"} placement={"right"}>
                            <IconButton onClick={closeSidebar}>
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                     fill="none"
                                     stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                     stroke-linejoin="round"
                                     className="lucide lucide-table-2">
                                    <path
                                        d="M9 3H5a2 2 0 0 0-2 2v4m6-6h10a2 2 0 0 1 2 2v4M9 3v18m0 0h10a2 2 0 0 0 2-2V9M9 21H5a2 2 0 0 1-2-2V9m0 0h18"/>
                                </svg>
                            </IconButton>
                        </Tooltip>
                    </div>
                </Col>
                <Col className={"justify-center items-end align-middle w-1/2"}>
                    <div className="flex justify-center items-center">
                        <Tooltip content={"New Chat"} placement={"right"}>
                            <IconButton>
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                     fill="none"
                                     stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                     stroke-linejoin="round"
                                     className="lucide lucide-square-pen">
                                    <path d="M12 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                                    <path
                                        d="M18.375 2.625a1 1 0 0 1 3 3l-9.013 9.014a2 2 0 0 1-.853.505l-2.873.84a.5.5 0 0 1-.62-.62l.84-2.873a2 2 0 0 1 .506-.852z"/>
                                </svg>
                            </IconButton>
                        </Tooltip>
                    </div>
                </Col>
            </Row>
        </Row>
    )
}

export default Sidebar;
