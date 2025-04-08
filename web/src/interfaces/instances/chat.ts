import { MessageInterface } from "./message";
import { BaseModel } from "./base";

export interface ChatInterface extends BaseModel{
    user_id: string,
    messages: MessageInterface[]
}
