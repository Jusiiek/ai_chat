import React from "react";
import {useDispatch, useSelector} from "react-redux";
import {useNavigate} from "react-router-dom";

import {setSidebarState} from "../reducers/siderbar";
import {setModalState} from "../reducers/modal";
import {
    Row,
    Col,
    Avatar,
    Tooltip,
    IconButton,
    Dropdown,
    Text,
    Icon
} from "../components";
import {RootState} from "../store";
import { AuthService } from "../services/auth";
import { ActiveUser } from "../instances/user";
import { PATHS } from "../router/routes";

interface NavbarProps {
    className?: string
}

const Navbar: React.FC<NavbarProps> = ({className}) => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const isSidebarOpen = useSelector((state: RootState) => state.sidebar.isOpen);

    const openSidebar = () => {
        dispatch(setSidebarState(true));
    }

    const openSettingsModal = () => {
        dispatch(setModalState(true));
    }

    const handleLogout =  async () => {
        await AuthService.logout();
        ActiveUser.clear();
        navigate(PATHS.LOGIN, { replace: true });
    }

    return (
        <Row className={`w-full h-full bg-white dark:bg-gray-900 py-[18px] px-[12px] ${className}`}>
            <Col className={"justify-center items-start w-1/2"}>
                <Row className={"items-center"}>
                    {
                        !isSidebarOpen ?
                            <div>
                                <Tooltip content={"Open sidebar"} placement={"right"}>
                                    <IconButton onClick={openSidebar}>
                                        <Icon name={"table"} />
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
                                        <Icon name={"square-pen"} />
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
                    <Dropdown>
                        <Dropdown.Trigger>
                            <Avatar/>
                        </Dropdown.Trigger>
                        <Dropdown.Menu className="py-1">
                            <Dropdown.MenuItem onClick={openSettingsModal}>
                                <Text size={"base"}>
                                    Settings
                                </Text>
                            </Dropdown.MenuItem>
                            <Dropdown.MenuItem onClick={handleLogout}>
                                <Text size={"base"} className={"text-red-600"}>
                                    Logout
                                </Text>
                            </Dropdown.MenuItem>
                        </Dropdown.Menu>
                    </Dropdown>
                </Row>
            </Col>
        </Row>
    );
};

export default Navbar;
