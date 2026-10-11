"use client";
import Link from "next/link";
import { useAuth } from "@/lib/auth";
import { Button } from "@/components/ui/button";
import { Utensils, CalendarDays, ShoppingBag, Sparkles, User, LogOut } from "lucide-react";

export function Navbar() {
  const { user, logout } = useAuth();
  return (
    <nav className="border-b bg-white">
      <div className="container mx-auto flex h-16 items-center justify-between">
        <Link href="/" className="flex items-center gap-2 text-xl font-bold text-primary">
          <Utensils className="h-6 w-6" /> RestaurantAI
        </Link>
        <div className="flex items-center gap-4 text-sm">
          <Link href="/restaurants" className="flex items-center gap-1 hover:text-primary"><Utensils className="h-4 w-4" />Restaurants</Link>
          {user && <>
            <Link href="/assistant" className="flex items-center gap-1 hover:text-primary"><Sparkles className="h-4 w-4" />AI Assistant</Link>
            <Link href="/reservations" className="flex items-center gap-1 hover:text-primary"><CalendarDays className="h-4 w-4" />Reservations</Link>
            <Link href="/orders" className="flex items-center gap-1 hover:text-primary"><ShoppingBag className="h-4 w-4" />Orders</Link>
          </>}
        </div>
        <div className="flex items-center gap-2">
          {user ? (
            <>
              <Link href="/profile" className="flex items-center gap-1 text-sm hover:text-primary"><User className="h-4 w-4" />{user.name}</Link>
              <Button variant="outline" size="sm" onClick={logout}><LogOut className="mr-1 h-4 w-4" />Logout</Button>
            </>
          ) : (
            <>
              <Link href="/login"><Button variant="outline" size="sm">Login</Button></Link>
              <Link href="/register"><Button size="sm">Sign Up</Button></Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}