// Navbar.tsx
import React from "react";
import {
    Row,
    Col,
    ThemeSwitcher,
    Avatar
} from "../components";

interface NavbarProps {
    className?: string
}

const Navbar: React.FC<NavbarProps> = ({className}) => {
    return (
        <Row className={`w-full h-full bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-600 p-4 ${className}`}>
            <Col className={"justify-start items-start w-1/2"}>
                <Row className={"items-center"}>
                    <div>OPEN SIDEBAR ICON</div>
                    <div>NEW CHAT ICON</div>
                    <div>MODEL NAME</div>
                </Row>
            </Col>
            <Col className={"justify-end items-end w-1/2"}>
                <Row className={"items-center"}>
                    <ThemeSwitcher className={"mr-3"} />
                    <Avatar />
                </Row>
            </Col>
        </Row>
    );
};

export default Navbar;
