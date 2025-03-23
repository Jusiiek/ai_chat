import { ServiceReturnInterface } from "@/interfaces/services/base";

export interface RequestParams {
    url: string;
    query?: Record<string, string | number | boolean>;
    headers?: Record<string, string>;
    method?: "GET" | "POST" | "PUT" | "DELETE" | "PATCH";
    body?: Record<string, any>;
    formData?: FormData;
    skipRedirect?: boolean;
    [key: string]: any;
}

export interface RequestResponse extends ServiceReturnInterface {
    headers: Headers
}