import React from 'react';
import {useDispatch, useSelector} from 'react-redux';

import {RootState} from "../store";
import {setModalState} from "../reducers/modal";
import {
    Row,
    Col,
    Text,
    IconButton,
    Icon
} from "../components";
import {IconName} from "./Icon";


interface Setting {
    icon: IconName;
    title: string;
}

const SettingsModal: React.FC = () => {
    const dispatch = useDispatch();
    const isOpen = useSelector((state: RootState) => state.modal.isOpen);

    const closeModal = () => {
        dispatch(setModalState(false))
    }

    const settingsList: Setting[] = [
        {
            icon: "settings",
            title: "General"
        },
        {
            icon: "user",
            title: "Personalization"
        }
    ]

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 overflow-y-auto">
            <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
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
                                        className="flex items-center p-3 rounded-md bg-gray-700/50 md:bg-transparent hover:bg-gray-700/70 cursor-pointer
                                        md:w-full w-auto flex-grow md:flex-grow-0 md:mb-2"
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

                            {/* Settings content area */}
                            <div className="w-full md:w-3/4 mt-6 md:mt-0 md:pl-6">
                                {/* Your settings content goes here */}
                                <div className="mb-6">
                                    <h2 className="text-xl mb-4">Theme</h2>
                                    {/* Theme settings */}
                                </div>

                                {/* Other settings */}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SettingsModal;
