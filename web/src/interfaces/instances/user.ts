export interface TokenInterface {
    access_token: string;
    token_type: string
}

export interface UserInterface {
    id: string
    email: string
    is_active: boolean
    is_superuser: boolean
    is_verified: boolean
}
