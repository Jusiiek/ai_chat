import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";

import {
    Card,
    Button,
    Input,
    Row,
    Col,
    Text
} from "../components";
import { AuthService } from "../services/auth";
import { UsersService } from "../services/user";
import { PATHS } from "../router/routes";
import { ActiveUser } from "../instances/user";
import { setAlertState } from "../reducers/alert";

const Login = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        email: "",
        password: "",
    });
    const [isButtonDisabled, setIsButtonDisabled] = useState(true);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const showAlert = (message?: string) => {
        dispatch(setAlertState({
            show: true,
            content: message || "Invalid email or password",
            color: "danger"
        }))
    }

    const handleLogin = async () => {
        try {
            if (!isButtonDisabled) {
                const { res } = await AuthService.login(formData);
                if (res.status === 200) {
                    const { data } = await UsersService.fetchCurrentUser();
                    ActiveUser.set(data);
                    navigate(PATHS.HOME, { replace: true });
                } else
                    showAlert();
            }
        } catch (error) {
            showAlert();
        }
    };

    const validateForm = () => {
        const isFilled = Object.values(formData).every((value) => value !== "");
        setIsButtonDisabled(!isFilled);
    };

    useEffect(() => {
        validateForm();
    }, [formData]);

    return (
        <div
            className={'h-full w-full flex items-center justify-center'}
        >
            <Card
                className={"w-full max-w-6/12"}
                style={{maxWidth: 500}}
            >
                <Row className={"w-full text-center mb-5"}>
                    <Text
                        size="3xl"
                        weight="bold"
                        className="ml-auto mr-auto"
                    >
                        Welcome back
                    </Text>
                </Row>
                {
                    Object.keys(formData).map((field) => (
                        <Row className={"w-full text-center mb-4"} key={field}>
                            <Input
                                id={field}
                                name={field}
                                label={field.replace("_", " ").toUpperCase()}
                                type={field === "password" ? "password" : "text"}
                                onChange={handleInputChange}
                                value={formData[field as keyof typeof formData]}
                                data-cy={`login-input-${field}`}
                            />
                        </Row>
                    ))
                }
                <Row className={"w-full text-center"}>
                    <Col className={"w-50"}>
                        <Button
                            variant={"secondary"}
                            className={"mr-auto"}
                            to={PATHS.REGISTER}
                        >
                            Create an account
                        </Button>
                    </Col>
                    <Col className={"w-50 text-right ml-auto"}>
                        <Button
                            variant={"primary"}
                            className={"ml-auto"}
                            disabled={isButtonDisabled}
                            onClick={handleLogin}
                            data-cy={"login-button"}
                        >
                            Login
                        </Button>
                    </Col>
                </Row>
            </Card>
        </div>
    )
}

export default Login;