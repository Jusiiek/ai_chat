import React, { useState, useEffect } from "react";

import {
    Card,
    Button,
    Input,
    Row,
    Col,
    Text
} from "@components/index.tsx";


const Register = () => {

    const [formData, setFormData] = useState({
        email: "",
        password: "",
        repeat_password: ""
    });
    const [isButtonDisabled, setIsButtonDisabled] = useState(true);
    const [loginError, setLoginError] = useState("");

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const handleRegister = async () => {
        try {
          // Implement your login logic here
          // Example:
          // const response = await axios.post('/api/auth/signin', formData);
          // console.log(response);
            setLoginError("");
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
                <Row className={"w-full text-center mb-4"}>
                    <Text
                        size={"4xl"}
                        weight={"bold"}
                        className={"ml-auto mr-auto"}>
                        Register
                    </Text>
                </Row>
                {
                    Object.keys(formData).map((key) => (
                        <Row className={"w-full text-center mb-4"}>
                            <Input
                                id={key}
                                name={key}
                                label={key.replace("_", " ").split(" ")
                                    .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
                                    .join(" ")}
                                type={key.includes("password") ? "password" : "text"}
                                onChange={handleInputChange}
                                value={formData[key as keyof typeof formData]}
                            />
                        </Row>
                    ))
                }
                <Row className={"w-full text-center"}>
                    <Col className={"w-50"}>
                        <Button
                            variant={"secondary"}
                            className={"mr-auto"}
                            to={"/auth/login"}
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