import { BaseModel } from "./base";


export interface MessageInterface extends BaseModel {
    chat_id: string,
    author_role: string,
    content: string,
    isLoading?: boolean
}
