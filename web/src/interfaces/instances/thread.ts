import { ChatInterface } from "./chat";
import { BaseModel } from "./base";

export interface ThreadListItemInterface {
    id: string;
    title: string;
}

export type CategorizedThreads = Record<string, ThreadListItemInterface[]>;


export interface ThreadInterface extends BaseModel {
    title: string;
    user_id: string,
    conversations: ChatInterface[]
}
