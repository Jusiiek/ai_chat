import React, {useEffect, useState} from 'react';
import {useDispatch, useSelector} from 'react-redux';
import {useNavigate} from "react-router-dom";

import {RootState} from "../store";
import {setModalState} from "../reducers/modal";
import {
    Row,
    Col,
    Text,
    IconButton,
    Icon,
    ThemeSwitcher,
    Button,
    Input
} from "../components";
import {IconName} from "./Icon";
import { AuthService } from "../services/auth";
import { UsersService } from "../services/user";
import { ActiveUser } from "../instances/user";
import { PATHS } from "../router/routes";


interface Setting {
    icon: IconName;
    title: string;
}

const SettingsModal: React.FC = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        email: "",
        password: "",
        current_password: "",
        is_active: ActiveUser.getUser()?.is_active,
        is_superuser: ActiveUser.getUser()?.is_superuser,
        is_verified: ActiveUser.getUser()?.is_verified,
    })

    const currentEmail = ActiveUser.getUser()?.email;
    const [updateError, setUpdateError] = useState("");
    const [emailUpdateDisabled, setEmailUpdateDisabled] = useState(true);
    const [passwordUpdateDisabled, setPasswordUpdateDisabled] = useState(true);

    const isOpen = useSelector((state: RootState) => state.modal.isOpen);
    const [selectedSetting, setSelectedSetting] = useState('General');

    const closeModal = () => {
        dispatch(setModalState(false))
    }

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const handleUpdateEmail = async() => {
        try {
            if (!emailUpdateDisabled) {
                const userData = { ...formData } as Record<string, any>;
                delete userData["password"];
                delete userData["current_password"];
                const { res } = await UsersService.updateCurrentUser(formData);
                if (res.status === 200) {
                    await AuthService.logout();
                    ActiveUser.clear();
                    navigate(PATHS.LOGIN, { replace: true });
                } else {
                    setUpdateError("Invalid email or password");
                }
            }
        } catch (error) {
            setUpdateError("Invalid email or password");
        }
    }

    const handleUpdatePassword = async() => {
        try {
            if (!passwordUpdateDisabled) {
                const userData = { ...formData } as Record<string, any>;
                delete userData["email"];
                const { res } = await UsersService.updateCurrentUser(userData);
                if (res.status === 200) {
                    const { data } = await UsersService.fetchCurrentUser();
                    ActiveUser.set(data);
                } else {
                    setUpdateError("Invalid email or password");
                }
            }
        } catch (error) {
            setUpdateError("Invalid email or password");
        }
    }

    const validateForm = () => {
        const isEmailFilled = formData.email !== "";
        const isPasswordFilled = formData.password !== "" && formData.current_password !== "";
        setEmailUpdateDisabled(!isEmailFilled);
        setPasswordUpdateDisabled(!isPasswordFilled);
    };

    useEffect(() => {
        validateForm();
    }, [formData]);

    const handleLogout =  async () => {
        await AuthService.logout();
        ActiveUser.clear();
        navigate(PATHS.LOGIN, { replace: true });
    }

    const settingsList: Setting[] = [
        {
            icon: "settings",
            title: "General"
        },
        {
            icon: "user",
            title: "Account"
        }
    ]

    if (!isOpen) return null;

    const renderSettingContent = () => {
        switch (selectedSetting) {
            case 'General':
                return (
                    <>
                        <Row className="mb-6 w-full">
                            <Col className={"w-1/2"}>
                                <Text size={"lg"}>
                                    Theme
                                </Text>
                            </Col>
                            <Col className={"w-1/2 items-end"}>
                                <ThemeSwitcher className={"max-w-[56px]"} />
                            </Col>
                        </Row>

                        <Row className="mb-6 w-full">
                            <Col className={"w-1/2"}>
                                <Text size={"lg"}>
                                    Account
                                </Text>
                            </Col>
                            <Col className={"w-1/2 items-end"}>
                                <Button variant={"danger"} onClick={handleLogout}>
                                    <Text size={"base"}>
                                        Logout
                                    </Text>
                                </Button>
                            </Col>
                        </Row>
                    </>
                );

            case 'Account':
                return (
                    <>
                        <div className="mb-6">
                            <Text size={"lg"}>
                                Change email
                            </Text>
                            <div className="space-y-3">
                                <div>
                                    <Input
                                        label={"Current email"}
                                        name={"email"}
                                        type={"text"}
                                        value={currentEmail}
                                        disabled
                                    />
                                </div>
                                <div>
                                    <Input
                                        label={"New email"}
                                        name={"email"}
                                        type={"text"}
                                        onChange={handleInputChange}
                                        value={formData.email}
                                    />
                                </div>
                                <div className="text-right">
                                    <Button
                                        disabled={emailUpdateDisabled}
                                        onClick={handleUpdateEmail}
                                    >
                                        <Text size={"base"}>
                                            Update Email
                                        </Text>
                                    </Button>
                                </div>
                            </div>
                        </div>

                        <div className="mb-6">
                            <Text size={"lg"}>
                                Change Password
                            </Text>
                            <div className="space-y-3">
                                <div>
                                    <Input
                                        label={"Current password"}
                                        name={"current_password"}
                                        type={"password"}
                                        onChange={handleInputChange}
                                        value={formData.current_password}
                                    />
                                </div>
                                <div>
                                    <Input
                                        label={"New password"}
                                        name={"password"}
                                        type={"password"}
                                        onChange={handleInputChange}
                                        value={formData.password}
                                    />
                                </div>
                                <div className="text-right">
                                    <Button
                                        disabled={passwordUpdateDisabled}
                                        onClick={handleUpdatePassword}
                                    >
                                        <Text size={"base"}>
                                            Update Password
                                        </Text>
                                    </Button>
                                </div>

                            </div>
                        </div>
                    </>
                );

            default:
                return <div>Select a setting</div>;
        }
    };

    return (
        <div className="fixed inset-0 z-50 overflow-y-auto">
            <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:p-0">
                <div className="fixed inset-0 transition-opacity" onClick={closeModal}>
                    <div className="absolute inset-0 bg-black opacity-75"></div>
                </div>

                <div
                    className="inline-block align-bottom bg-white dark:bg-gray-900 text-gray-900 dark:text-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle w-full max-w-[700px] h-full max-h-[600px]"
                >
                    <div className="px-4 py-5 sm:px-6 sm:flex sm:flex-row-reverse">
                        <Row className={"w-full"}>
                            <Col className={"w-1/2"}>
                                <Text size={"lg"} weight={"bold"}>
                                    Settings
                                </Text>
                            </Col>
                            <Col className={"w-1/2 items-end"}>
                                <IconButton onClick={closeModal}>
                                    <Icon name={"x"}/>
                                </IconButton>
                            </Col>
                        </Row>
                    </div>

                    <div className="px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                        <div className="w-full flex flex-col md:flex-row">
                            <div className="w-full md:w-1/4 flex flex-row flex-wrap md:flex-col gap-2">
                                {settingsList.map(setting => (
                                    <div
                                        key={setting.title}
                                        className="flex items-center p-3 rounded-md
                                           bg-gray-300/50 dark:bg-gray-700/50
                                           md:bg-transparent md:dark:bg-transparent
                                           hover:bg-gray-300/70 dark:hover:bg-gray-700/70
                                           cursor-pointer"
                                        onClick={() => setSelectedSetting(setting.title)}
                                    >
                                        <Text size={"base"} className="mr-2">
                                            <Icon name={setting.icon}/>
                                        </Text>
                                        <Text size={"base"}>
                                            {setting.title}
                                        </Text>
                                    </div>
                                ))}
                            </div>

                            <div
                                className="w-full md:w-3/4 mt-6 md:mt-0 md:pl-6 max-h-[500px] overflow-y-scroll overflow-x-hidden">
                                {renderSettingContent()}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SettingsModal;
