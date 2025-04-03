import { MessageInterface } from "./message";

export interface ChatInterface {
    id: string
    user_id: string,
    created_at: Date,
    updated_at: Date,
    messages: MessageInterface[]
}
