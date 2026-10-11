"use client";
import { useEffect, useRef, useState } from "react";
import { useAuth } from "@/lib/auth";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Send, Sparkles, Loader2, CheckCircle2 } from "lucide-react";
import { RestaurantCard } from "@/components/RestaurantCard";
import { useSearchParams } from "next/navigation";
import { formatLKR } from "@/lib/utils";

type Msg = {
  role: "user" | "assistant" | "status";
  content: string;
  payload?: any;
  pending?: any;
};

export default function AssistantPage() {
  const { user } = useAuth();
  const searchParams = useSearchParams();
  const [messages, setMessages] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [conversationId, setConversationId] = useState<number | undefined>();
  const [activity, setActivity] = useState<string[]>([]);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);

  useEffect(() => {
    const q = searchParams.get("q");
    if (q && !input) setInput(q);
  }, [searchParams]);

  const send = async (text: string) => {
    if (!text.trim() || busy) return;
    setMessages((m) => [...m, { role: "user", content: text }]);
    setInput("");
    setBusy(true);
    setActivity([]);

    try {
      for await (const evt of api.agentStream({ conversation_id: conversationId, message: text })) {
        if (evt.type === "meta") {
          setConversationId(evt.data.conversation_id);
        } else if (evt.type === "status") {
          setActivity((a) => [...a, evt.data.message]);
        } else if (evt.type === "tool_call") {
          setActivity((a) => [...a, `● ${evt.data.name}`]);
        } else if (evt.type === "tool_result") {
          setActivity((a) => [...a, `✓ ${evt.data.name}`]);
        } else if (evt.type === "message") {
          setMessages((m) => [...m, {
            role: "assistant",
            content: evt.data.content,
            payload: evt.data.payload,
            pending: evt.data.pending,
          }]);
        } else if (evt.type === "error") {
          setMessages((m) => [...m, { role: "assistant", content: `Error: ${evt.data.message}` }]);
        }
      }
    } catch (e: any) {
      setMessages((m) => [...m, { role: "assistant", content: `Error: ${e.message}` }]);
    } finally {
      setBusy(false);
    }
  };

  if (!user) return <div className="p-12 text-center">Please <a className="text-primary underline" href="/login">login</a> to use the agent.</div>;

  const suggestions = [
    "Find an Italian restaurant in Colombo for 4 people tomorrow at 7:30 PM under Rs. 8,000",
    "Show me cheap Chinese restaurants in Colombo",
    "What can I order at Italian Garden?",
    "Show my reservations",
  ];

  return (
    <div className="mx-auto flex h-[80vh] max-w-4xl flex-col rounded-xl border bg-white shadow">
      <div className="flex items-center gap-2 border-b p-4">
        <Sparkles className="h-5 w-5 text-primary" />
        <h2 className="font-semibold">Restaurant AI Agent</h2>
        {conversationId && <Badge>conv #{conversationId}</Badge>}
      </div>

      <div className="flex-1 space-y-4 overflow-y-auto p-4">
        {messages.length === 0 && (
          <div className="space-y-3 pt-6 text-center text-muted-foreground">
            <Sparkles className="mx-auto h-10 w-10 text-primary" />
            <p>Ask me anything about restaurants, reservations, or orders.</p>
            <div className="mx-auto mt-4 grid max-w-xl gap-2">
              {suggestions.map((s) => (
                <button
                  key={s}
                  onClick={() => setInput(s)}
                  className="rounded-lg border bg-secondary/50 px-4 py-2 text-left text-sm hover:border-primary"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((m, i) => (
          <div key={i} className={m.role === "user" ? "flex justify-end" : "flex justify-start"}>
            <div className={`max-w-[85%] space-y-2 rounded-2xl px-4 py-2 ${m.role === "user" ? "bg-primary text-primary-foreground" : "bg-secondary"}`}>
              <p className="whitespace-pre-wrap text-sm">{m.content}</p>
              {m.pending && (
                <div className="rounded-lg border border-primary/30 bg-white p-2 text-xs text-primary">
                  Awaiting your confirmation...
                </div>
              )}
              {m.payload?.restaurants && (
                <div className="grid gap-2 md:grid-cols-2">
                  {m.payload.restaurants.slice(0, 4).map((r: any) => (
                    <RestaurantCard key={r.id} r={r} />
                  ))}
                </div>
              )}
              {m.payload?.reservation_id && (
                <div className="rounded-lg bg-white p-2 text-xs">
                  <CheckCircle2 className="inline h-3 w-3 text-green-600" /> Reservation #{m.payload.reservation_id} created
                </div>
              )}
              {m.payload?.order_id && (
                <div className="rounded-lg bg-white p-2 text-xs">
                  <CheckCircle2 className="inline h-3 w-3 text-green-600" /> Order #{m.payload.order_id} placed
                </div>
              )}
            </div>
          </div>
        ))}

        {busy && (
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Loader2 className="h-4 w-4 animate-spin" />
            <div className="space-y-1">
              {activity.slice(-4).map((a, i) => <p key={i} className="text-xs">{a}</p>)}
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <form
        onSubmit={(e) => { e.preventDefault(); send(input); }}
        className="flex items-center gap-2 border-t p-4"
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask the restaurant assistant..."
          className="flex-1 rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
          disabled={busy}
        />
        <Button type="submit" disabled={busy || !input.trim()} size="icon">
          <Send className="h-4 w-4" />
        </Button>
      </form>
    </div>
  );
}