import {
    Row, Col, Text
} from "../components";


function Home() {
    return (
        <div
            className={'h-full w-full flex items-center justify-center'}
        >
            <Col>
                <Text size={"3xl"} weight={"bold"}>
                    HERE WILL BE SIDEBAR
                </Text>
            </Col>
            <Col>
                <Row className={"w-full items-center justify-center text-center"}>
                    <Text size={"3xl"} weight={"bold"}>
                        Some header text!!!
                    </Text>
                </Row>
                <Row className={"w-full items-center justify-center text-center"}>
                    <Text size={"xl"} weight={"normal"}>
                        Some subheader text!!!
                    </Text>
                </Row>
            </Col>
        </div>
    )
}

export default Home;
