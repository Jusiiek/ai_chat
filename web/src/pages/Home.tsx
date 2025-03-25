import {
    Row,
    Col,
    Text,
    Navbar
} from "../components";


function Home() {
    return (
        <Row
            className={'h-full w-full'}
        >
            <Col className={"overflow-hidden"}>
                <Text size={"3xl"} weight={"bold"}>
                    HERE WILL BE SIDEBAR
                </Text>
            </Col>
            <Col className={"w-auto flex-1"}>
                <Row className={"w-full items-center justify-center text-center"}>
                    <Navbar />
                </Row>
                <Row className={"w-full items-center justify-center text-center"}>
                    <Text size={"xl"} weight={"normal"}>
                        Some subheader text!!!
                    </Text>
                </Row>
            </Col>
        </Row>
    )
}

export default Home;
