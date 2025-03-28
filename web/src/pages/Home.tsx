import React, { useState } from "react";

import {
    Row,
    Col,
    Text,
    Navbar,
    Sidebar
} from "../components";


function Home() {
    const [openSidebar, setOpenSidebar] = useState(true);
    return (
        <Row className={'h-full w-full'}>
            <Col style={{width: `${openSidebar ? '300px' : '0px'}`}}>
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
