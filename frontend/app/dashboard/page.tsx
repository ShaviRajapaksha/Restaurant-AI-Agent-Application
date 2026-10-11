"use client";
import { useAuth } from "@/lib/auth";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Sparkles, Utensils, CalendarDays, ShoppingBag } from "lucide-react";
import Link from "next/link";

export default function Dashboard() {
  const { user } = useAuth();
  if (!user) return <div className="p-12 text-center">Please <a className="text-primary underline" href="/login">login</a>.</div>;
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">Welcome, {user.name}</h1>
        <p className="text-muted-foreground">What would you like to do today?</p>
      </div>
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {[
          { href: "/assistant", icon: Sparkles, label: "Ask the AI Agent", desc: "Book or order with a chat" },
          { href: "/restaurants", icon: Utensils, label: "Browse Restaurants", desc: "Search and filter" },
          { href: "/reservations", icon: CalendarDays, label: "My Reservations", desc: "View and manage" },
          { href: "/orders", icon: ShoppingBag, label: "My Orders", desc: "Track your food" },
        ].map(({ href, icon: Icon, label, desc }) => (
          <Link key={href} href={href}>
            <Card className="h-full transition hover:border-primary">
              <CardHeader>
                <Icon className="h-8 w-8 text-primary" />
                <CardTitle className="pt-2">{label}</CardTitle>
              </CardHeader>
              <CardContent className="text-sm text-muted-foreground">{desc}</CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}