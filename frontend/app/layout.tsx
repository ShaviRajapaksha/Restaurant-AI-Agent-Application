import "./globals.css";
import type { Metadata } from "next";
import { AuthProvider } from "@/lib/auth";
import { Navbar } from "./../components/Navbar";
import { QueryProvider } from "./../components/QueryProvider";

export const metadata: Metadata = { title: "Restaurant AI Agent", description: "AI-powered restaurant discovery and reservations" };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-background">
        <QueryProvider>
          <AuthProvider>
            <Navbar />
            <main className="container mx-auto py-8">{children}</main>
          </AuthProvider>
        </QueryProvider>
      </body>
    </html>
  );
}