import React, {useState} from "react";

import {
    Card,
    Button,
    Input,
    Row,
    Col,
    Text
} from "@components/index.tsx";


const Login = () => {

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [isButtonDisabled, setIsButtonDisabled] = useState(true);
    const [loginError, setLoginError] = useState("");


    const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setEmail(e.target.value);
    };

    const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setPassword(e.target.value);
    };

    const handleLogin = async () => {
        try {
      // Implement your login logic here
      // For example, using Axios or fetch to send a request to your backend
      // const response = await axios.post('/api/auth/signin', { email, password });
      // console.log(response);
        setLoginError("");
        } catch (error) {
            setLoginError("Invalid email or password");
        }
    };

    const validateForm = () => {
        if (email && password) {
            setIsButtonDisabled(false);
        } else {
            setIsButtonDisabled(true);
        }
    };

    React.useEffect(() => {
        validateForm();
    }, [email, password]);

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
                        Login
                    </Text>
                </Row>
                <Row className={"w-full text-center mb-4"}>
                    <Input
                        label={"Email"}
                        value={email}
                        onChange={handleEmailChange}
                    />
                </Row>
                <Row className={"w-full text-center mb-4"}>
                    <Input
                        label={"Password"}
                        type={"password"}
                        value={password}
                        onChange={handlePasswordChange}
                    />
                </Row>
                <Row className={"w-full text-center"}>
                    <Col className={"w-50"}>
                        <Button
                            variant={"secondary"}
                            className={"mr-auto"}
                        >
                            Register
                        </Button>
                    </Col>
                    <Col className={"w-50 text-right ml-auto"}>
                        <Button
                            variant={"primary"}
                            className={"ml-auto"}
                            disabled={isButtonDisabled}
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