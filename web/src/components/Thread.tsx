import React from "react";
import {
    Row,
    Conversation
} from "../components";

function Thread() {

    return (
        <Row className={"flex-1 grow basis-auto flex-col"}>
            <div
                className={"h-full overflow-y-scroll"}
            >
                <Conversation />
            </div>
        </Row>
    )
}

export default Thread;
