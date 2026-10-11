"use client";
import { useAuth } from "@/lib/auth";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function ProfilePage() {
  const { user } = useAuth();
  if (!user) return <p>Login required.</p>;
  return (
    <div className="mx-auto max-w-lg space-y-4">
      <h1 className="text-3xl font-bold">Profile</h1>
      <Card>
        <CardHeader><CardTitle>Account</CardTitle></CardHeader>
        <CardContent className="space-y-2 text-sm">
          <p><span className="text-muted-foreground">Name:</span> {user.name}</p>
          <p><span className="text-muted-foreground">Email:</span> {user.email}</p>
          <p><span className="text-muted-foreground">Role:</span> {user.role}</p>
        </CardContent>
      </Card>
    </div>
  );
}