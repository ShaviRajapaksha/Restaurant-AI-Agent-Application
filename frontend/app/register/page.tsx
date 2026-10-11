"use client";
import { useState } from "react";
import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function RegisterPage() {
  const { register } = useAuth();
  const router = useRouter();
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [err, setErr] = useState<string | null>(null);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);
    try {
      await register(form.name, form.email, form.password);
      router.push("/dashboard");
    } catch (e: any) {
      setErr(e.message);
    }
  };

  return (
    <div className="mx-auto max-w-md pt-12">
      <Card>
        <CardHeader>
          <CardTitle>Create account</CardTitle>
          <CardDescription>Start using the AI Restaurant Agent</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={onSubmit} className="space-y-4">
            <Input placeholder="Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
            <Input placeholder="Email" type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
            <Input placeholder="Password (min 6)" type="password" minLength={6} value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required />
            {err && <p className="text-sm text-destructive">{err}</p>}
            <Button type="submit" className="w-full">Register</Button>
            <p className="text-center text-sm text-muted-foreground">
              Have an account? <a className="text-primary underline" href="/login">Login</a>
            </p>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}