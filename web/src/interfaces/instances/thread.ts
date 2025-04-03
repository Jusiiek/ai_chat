import { ChatInterface } from "./chat";

export interface ThreadListItemInterface {
    id: string;
    title: string;
}

export type CategorizedThreads = Record<string, ThreadListItemInterface[]>;


export interface ThreadInterface extends ThreadListItemInterface{
    user_id: string,
    created_at: Date,
    updated_at: Date,
    conversations: ChatInterface[]
}
