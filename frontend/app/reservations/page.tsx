"use client";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useAuth } from "@/lib/auth";

export default function ReservationsPage() {
  const { user } = useAuth();
  const qc = useQueryClient();
  const { data, isLoading } = useQuery({ queryKey: ["reservations"], queryFn: api.listReservations, enabled: !!user });

  if (!user) return <p>Login required.</p>;

  const cancel = async (id: number) => {
    if (!confirm("Cancel this reservation?")) return;
    await api.cancelReservation(id);
    qc.invalidateQueries({ queryKey: ["reservations"] });
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">My Reservations</h1>
      {isLoading && <p>Loading...</p>}
      <div className="grid gap-4 md:grid-cols-2">
        {data?.map((r: any) => (
          <Card key={r.id}>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                Reservation #{r.id}
                <Badge>{r.status}</Badge>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 text-sm">
              <p>Restaurant: <span className="font-semibold">#{r.restaurant_id}</span></p>
              <p>Date: <span className="font-semibold">{r.reservation_date}</span></p>
              <p>Time: <span className="font-semibold">{r.reservation_time}</span></p>
              <p>Party: <span className="font-semibold">{r.party_size}</span></p>
              {r.status !== "CANCELLED" && (
                <Button variant="destructive" size="sm" onClick={() => cancel(r.id)}>Cancel</Button>
              )}
            </CardContent>
          </Card>
        ))}
        {data?.length === 0 && <p className="text-muted-foreground">No reservations yet.</p>}
      </div>
    </div>
  );
}