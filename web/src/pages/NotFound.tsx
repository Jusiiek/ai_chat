import React from "react";
import {useNavigate} from "react-router-dom";

import {
    Row,
    Col,
    Text,
    Button
} from "../components";
import {ActiveUser} from "../instances/user";
import {PATHS} from "../router/routes";

const NotFound = () => {
    const navigate = useNavigate();
    const navigateUser = () => {
        const user = ActiveUser.getUser();

        if (!user)
            return navigate(PATHS.LOGIN, {replace: true});
        return navigate(PATHS.HOME, {replace: true});
    }

    return (
        <Row className="items-center justify-center h-screen text-center">
            <Col className={"w-full"}>
                <Col className={"w-full mb-3"}>
                    <Text size={"5xl"} weight={"extrabold"}>
                        404
                    </Text>
                </Col>
                <Col className={"w-full mb-3"}>
                    <Text size={"2xl"} weight={"bold"}>
                        The page you're looking for does not exist.
                    </Text>
                </Col>
                <Col className={"w-full justify-center items-center"}>
                    <Button
                        size={"large"}
                        className={"max-w-[200px]"}
                        onClick={navigateUser}
                    >
                        Leave
                    </Button>
                </Col>
            </Col>
        </Row>
    );
};

export default NotFound;
