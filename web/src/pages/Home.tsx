import React from "react";
import { useSelector } from 'react-redux';

import {
    Row,
    Col,
    Text,
    Navbar,
    Sidebar
} from "../components";
import { RootState } from "../store";


function Home() {
    const isSidebarOpen = useSelector((state: RootState) => state.sidebar.isOpen);
    return (
        <Row className={'h-full w-full'}>
            <Col
                style={{width: `${isSidebarOpen ? '300px' : '0px'}`}}
                className={"h-full transition-all duration-300 ease-in-out"}
            >
                <Sidebar />
            </Col>
            <Col className={"w-auto flex-1"}>
                <Row className={"w-full items-center justify-center text-center"}>
                    <Navbar />
                </Row>
                <Row className={"w-full items-center justify-center text-center"}>
                    <Text size={"xl"} weight={"normal"}>
                        Some subheader text!!!
                    </Text>
                </Row>
            </Col>
        </Row>
    )
}

export default Home;
