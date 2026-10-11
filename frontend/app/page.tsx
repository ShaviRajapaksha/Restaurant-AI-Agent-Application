import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Sparkles, Utensils, CalendarCheck } from "lucide-react";

export default function Home() {
  return (
    <div className="space-y-16 py-12 text-center">
      <section className="space-y-6">
        <h1 className="text-5xl font-bold tracking-tight">
          Meet your <span className="text-primary">AI Restaurant Agent</span>
        </h1>
        <p className="mx-auto max-w-2xl text-lg text-muted-foreground">
          Discover restaurants, check availability, and book tables entirely through natural conversation.
          Not a chatbot — a real agent that takes action.
        </p>
        <div className="flex justify-center gap-4">
          <Link href="/assistant"><Button size="lg"><Sparkles className="mr-2 h-5 w-5" />Try the Agent</Button></Link>
          <Link href="/restaurants"><Button size="lg" variant="outline"><Utensils className="mr-2 h-5 w-5" />Browse Restaurants</Button></Link>
        </div>
      </section>

      <section className="grid gap-6 md:grid-cols-3">
        {[
          { icon: Sparkles, title: "Conversational", text: "Ask in plain English. The agent asks for what it needs and remembers context." },
          { icon: Utensils, title: "Real Tool Use", text: "Searches restaurants, checks tables, retrieves menus — via real API tools." },
          { icon: CalendarCheck, title: "Confirm & Book", text: "The agent asks for confirmation before creating reservations or orders." },
        ].map(({ icon: Icon, title, text }) => (
          <div key={title} className="rounded-xl border bg-white p-6 text-left">
            <Icon className="mb-3 h-8 w-8 text-primary" />
            <h3 className="mb-2 text-lg font-semibold">{title}</h3>
            <p className="text-sm text-muted-foreground">{text}</p>
          </div>
        ))}
      </section>
    </div>
  );
}