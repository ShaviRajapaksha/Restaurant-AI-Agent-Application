const BASE = ""; // rewrites handle proxying to backend

export type ApiError = { detail: string };

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("token");
}

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(init.headers as Record<string, string> | undefined),
  };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${BASE}${path}`, { ...init, headers });
  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(body.detail || "Request failed");
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

export const api = {
  // auth
  register: (data: { name: string; email: string; password: string }) =>
    request("/api/auth/register", { method: "POST", body: JSON.stringify(data) }),
  login: (data: { email: string; password: string }) =>
    request<{ access_token: string }>("/api/auth/login", { method: "POST", body: JSON.stringify(data) }),
  me: () => request<{ id: number; name: string; email: string; role: string }>("/api/auth/me"),

  // restaurants
  listRestaurants: (params: Record<string, string | number | undefined> = {}) => {
    const q = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => v !== undefined && v !== "" && q.set(k, String(v)));
    return request<{ items: any[]; total: number }>(`/api/restaurants?${q.toString()}`);
  },
  getRestaurant: (id: number) => request<any>(`/api/restaurants/${id}`),
  getMenu: (id: number) => request<any[]>(`/api/restaurants/${id}/menu`),

  // reservations
  listReservations: () => request<any[]>("/api/reservations"),
  createReservation: (data: any) => request<any>("/api/reservations", { method: "POST", body: JSON.stringify(data) }),
  cancelReservation: (id: number) => request<any>(`/api/reservations/${id}`, { method: "DELETE" }),

  // orders
  listOrders: () => request<any[]>("/api/orders"),

  // conversations
  listConversations: () => request<any[]>("/api/conversations"),
  getMessages: (cid: number) => request<any[]>(`/api/conversations/${cid}/messages`),

  // agent (SSE)
  agentStreamUrl: "/api/agent/chat",
  agentStream: async function* (body: { conversation_id?: number; message: string }) {
    const token = getToken();
    const res = await fetch("/api/agent/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify(body),
    });
    if (!res.body) throw new Error("No stream");
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buf = "";
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += decoder.decode(value, { stream: true });
      const parts = buf.split("\n\n");
      buf = parts.pop() || "";
      for (const part of parts) {
        const line = part.replace(/^data:\s*/, "");
        if (!line) continue;
        try {
          yield JSON.parse(line);
        } catch {}
      }
    }
  },
};