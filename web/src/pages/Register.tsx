import React, { useState, useEffect } from "react";

import {
    Card,
    Button,
    Input,
    Row,
    Col,
    Text
} from "../components";
import { AuthService } from "../services/auth";
import { PATHS } from "../router/routes";


const Register = () => {

    const [formData, setFormData] = useState({
        email: "",
        password: "",
        repeat_password: ""
    });
    const [isButtonDisabled, setIsButtonDisabled] = useState(true);
    const [loginError, setLoginError] = useState("");

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        console.log("[e.target.id]: e.target.value ", [e.target.id], e.target.value )
        setFormData((prev) => ({
            ...prev,
            [e.target.id]: e.target.value
        }));
    };

    const handleRegister = async () => {
        try {
            const isFilled = Object.values(formData).every((value) => value.trim() !== "");
            const isPasswordValid = formData.repeat_password === formData.password
            if (isFilled && isPasswordValid) {
                let body = {
                    email: formData.email,
                    password: formData.password,
                };
                await AuthService.register(body);
                setLoginError("");
            }
        } catch (error) {
            setLoginError("Invalid email or password");
        }
    };

    const validateForm = () => {
        const isValid = Object.values(formData).every((value) => value.trim() !== "");
        setIsButtonDisabled(!isValid);
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
                        Create your account
                    </Text>
                </Row>
                {
                    Object.keys(formData).map((field) => (
                        <Row className={"w-full text-center mb-4"} key={field}>
                            <Input
                                id={field}
                                name={field}
                                label={field.replace("_", " ").split(" ")
                                    .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
                                    .join(" ")}
                                type={field.includes("password") ? "password" : "text"}
                                onChange={handleInputChange}
                                value={formData[field as keyof typeof formData]}
                            />
                        </Row>
                    ))
                }
                <Row className={"w-full text-center"}>
                    <Col className={"w-50"}>
                        <Button
                            variant={"secondary"}
                            className={"mr-auto"}
                            to={PATHS.LOGIN}
                        >
                            Back to login
                        </Button>
                    </Col>
                    <Col className={"w-50 text-right ml-auto"}>
                        <Button
                            variant={"primary"}
                            className={"ml-auto"}
                            disabled={isButtonDisabled}
                        >
                            Register
                        </Button>
                    </Col>
                </Row>
            </Card>
        </div>
    )
}

export default Register;
