"use client";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { formatLKR } from "@/lib/utils";
import { useAuth } from "@/lib/auth";

export default function OrdersPage() {
  const { user } = useAuth();
  const { data, isLoading } = useQuery({ queryKey: ["orders"], queryFn: api.listOrders, enabled: !!user });
  if (!user) return <p>Login required.</p>;
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">My Orders</h1>
      {isLoading && <p>Loading...</p>}
      <div className="grid gap-4 md:grid-cols-2">
        {data?.map((o: any) => (
          <Card key={o.id}>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                Order #{o.id} <Badge>{o.status}</Badge>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 text-sm">
              <p>Restaurant: #{o.restaurant_id}</p>
              {o.items.map((it: any) => (
                <p key={it.id}>{it.quantity} × {it.name_snapshot} — {formatLKR(it.unit_price * it.quantity)}</p>
              ))}
              <p className="border-t pt-2 font-bold">Total: {formatLKR(o.total_amount)}</p>
            </CardContent>
          </Card>
        ))}
        {data?.length === 0 && <p className="text-muted-foreground">No orders yet.</p>}
      </div>
    </div>
  );
}