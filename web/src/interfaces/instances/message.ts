export interface MessageInterface {
    id: string,
    chat_id: string,
    author_role: string,
    content: string,
    created_at: Date,
    updated_at: Date,
    isLoading?: boolean
}
