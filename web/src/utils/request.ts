import { RequestParams, RequestResponse } from "@interfaces/utils/request.ts";
import { ActiveUser } from "@instances/user.ts";


export const redirectIfNotAuthenticated = (res: Response) => {
  if (res.status === 401) {
    return window.location.replace("/auth/login");
  }
  if (res.status === 403) return window.location.replace("/");
};

export const encodeQuery = (query: Record<string, any>) => {
  const searchParams = new URLSearchParams(query || {});
  return searchParams.toString();
};

export const request = async ({
  url,
  query,
  headers = {},
  method = "GET",
  body,
  formData,
  skipRedirect = false,
  ...rest
}: RequestParams): Promise<RequestResponse> => {
  const methodLower = method.toLowerCase();
  const jsonMethods = ["post", "put", "patch", "delete"];
  if (body && jsonMethods.includes(methodLower) && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }
  if (body && typeof body === "object") {
    body = JSON.stringify(body);
  }
  if (formData) {
    body = formData;
  }
  const token = ActiveUser.getToken()
  const tokenType = ActiveUser.getTokenType()
  if (token && tokenType) {
    headers.Authorization = `${tokenType} ${token}`;
  }

  if (query) {
    url = `${url}?${encodeQuery(query)}`;
  }
  const res = await fetch(url, {
    method: method,
    headers: headers,
    body: body,
    credentials: "include",
    ...rest,
  });

  if (!skipRedirect) {
    redirectIfNotAuthenticated(res);
  }

  const contentType = res.headers.get("content-type");
  if (contentType !== "application/json" || res.status === 204) {
    return {
      res,
      data: {},
      headers: res.headers,
    };
  }

  const data = await res.json();

  return {
    res,
    data,
    headers: res.headers,
  };
};
