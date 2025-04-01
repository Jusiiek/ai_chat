import React from "react";
import { useSelector } from 'react-redux';

import {
    Row,
    Col,
    Navbar,
    Sidebar,
    SettingsModal,
    Thread
} from "../components";
import { RootState } from "../store";


function Home() {
    const isSidebarOpen = useSelector((state: RootState) => state.sidebar.isOpen);
    return (
        <Row className={'h-full w-full overflow-hidden'}>
            <SettingsModal />
            <Col
                className={`h-full transition-all duration-300 ease-in-out ${isSidebarOpen ? 'w-[300px]' : 'w-0'}`}
            >
                <Sidebar />
            </Col>
            <Col className={"w-auto flex-1"}>
                <Row className={"w-full items-center justify-center text-center"}>
                    <Navbar />
                </Row>
                <Row className={"w-full items-center justify-center text-center"}>
                    <Thread />
                </Row>
            </Col>
        </Row>
    )
}

export default Home;
