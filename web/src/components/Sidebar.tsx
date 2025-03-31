import React from 'react';
import { useDispatch } from "react-redux";

import { setSidebarState } from "../reducers/siderbar";

import {
    Row,
    Col,
    Tooltip,
    IconButton,
    Icon
} from "../components";


const Sidebar: React.FC = () => {
    const dispatch = useDispatch();

    const closeSidebar = () => {
        dispatch(setSidebarState(false));
    }

    return (
        <nav className={"d-flex w-full h-full bg-gray-800 text-white overflow-hidden"}>
            <Row className={`w-full py-[23px] px-[12px]`}>
                <Col className={"justify-start items-start align-middle w-1/2"}>
                    <div className="flex justify-center items-center">
                        <Tooltip content={"Close sidebar"} placement={"right"}>
                            <IconButton onClick={closeSidebar}>
                                <Icon name={"table"} />
                            </IconButton>
                        </Tooltip>
                    </div>
                </Col>
                <Col className={"justify-start items-end align-middle w-1/2"}>
                    <div className="flex justify-center items-center">
                        <Tooltip content={"New Chat"} placement={"left"}>
                            <IconButton>
                                <Icon name={"square-pen"} />
                            </IconButton>
                        </Tooltip>
                    </div>
                </Col>
            </Row>
        </nav>
    )
}

export default Sidebar;
