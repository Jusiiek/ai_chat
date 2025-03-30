import React from 'react';
import { useDispatch, useSelector } from 'react-redux';

import {RootState} from "../store";
import { setModalState } from "../reducers/modal";
import {
    Row,
    Col,
    Text,
    IconButton,
    Icon
} from "../components";

const SettingsModal: React.FC = () => {
    const dispatch = useDispatch();
    const isOpen = useSelector((state: RootState) => state.modal.isOpen);

    const closeModal = () => {
        dispatch(setModalState(false))
    }

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 overflow-y-auto">
            <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                <div className="fixed inset-0 transition-opacity" onClick={closeModal}>
                    <div className="absolute inset-0 bg-black opacity-75"></div>
                </div>

                <div
                    className="inline-block align-bottom bg-white dark:bg-gray-900 text-gray-900 dark:text-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full"
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
                                    <Icon name={"x"} />
                                </IconButton>
                            </Col>
                        </Row>
                    </div>

                    <div className="px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                        <Row className={"w-full"}>
                            <Col className={"w-1/4"}>
                                <Row className={"w-full"}>
                                    <Text size={"base"}>
                                        General
                                    </Text>
                                </Row>
                                <Row className={"w-full"}>
                                    <Text size={"base"}>
                                        Personalization
                                    </Text>
                                </Row>
                            </Col>
                            <Col className={"w-3/4"}></Col>
                        </Row>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SettingsModal;
