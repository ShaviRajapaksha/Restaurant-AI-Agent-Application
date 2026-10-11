"use client";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { useParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Star, MapPin, Phone } from "lucide-react";
import { formatLKR } from "@/lib/utils";
import Link from "next/link";
import { Badge } from "@/components/ui/badge";

export default function RestaurantDetail() {
  const params = useParams();
  const id = Number(params.id);
  const { data: r } = useQuery({ queryKey: ["restaurant", id], queryFn: () => api.getRestaurant(id) });
  const { data: menu } = useQuery({ queryKey: ["menu", id], queryFn: () => api.getMenu(id) });

  if (!r) return <p>Loading...</p>;

  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-bold">{r.name}</h1>
          <p className="mt-1 flex items-center gap-2 text-muted-foreground">
            <MapPin className="h-4 w-4" /> {r.address}
            <Badge className="ml-2 flex items-center gap-1"><Star className="h-3 w-3 fill-yellow-400 text-yellow-400" />{r.rating}</Badge>
          </p>
          <p className="mt-1 text-muted-foreground"><Phone className="mr-1 inline h-4 w-4" />{r.phone}</p>
        </div>
        <Link href={`/assistant?q=${encodeURIComponent(`Reserve a table at ${r.name}`)}`}>
          <Button>Reserve with AI</Button>
        </Link>
      </div>

      <p className="text-muted-foreground">{r.description}</p>

      <div className="grid gap-4 md:grid-cols-3 text-sm">
        <Card><CardContent className="pt-6"><p className="text-muted-foreground">Cuisine</p><p className="font-semibold">{r.cuisine}</p></CardContent></Card>
        <Card><CardContent className="pt-6"><p className="text-muted-foreground">Average price</p><p className="font-semibold">{formatLKR(r.avg_price)}</p></CardContent></Card>
        <Card><CardContent className="pt-6"><p className="text-muted-foreground">Opening hours</p><p className="font-semibold">{r.opening_time} – {r.closing_time}</p></CardContent></Card>
      </div>

      <h2 className="pt-4 text-2xl font-bold">Menu</h2>
      {menu?.map((cat: any) => (
        <Card key={cat.id}>
          <CardHeader><CardTitle>{cat.name}</CardTitle></CardHeader>
          <CardContent className="space-y-2">
            {cat.items.map((item: any) => (
              <div key={item.id} className="flex items-center justify-between border-b pb-2 last:border-0">
                <div>
                  <p className="font-medium">{item.name}</p>
                  <p className="text-sm text-muted-foreground">{item.description}</p>
                </div>
                <p className="font-semibold">{formatLKR(item.price)}</p>
              </div>
            ))}
          </CardContent>
        </Card>
      ))}
    </div>
  );
}