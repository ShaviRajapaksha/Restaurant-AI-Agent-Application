import { Card, CardContent, CardFooter, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Star, MapPin } from "lucide-react";
import Link from "next/link";
import { formatLKR } from "@/lib/utils";

export function RestaurantCard({ r }: { r: any }) {
  return (
    <Card className="flex flex-col">
      <CardHeader>
        <div className="flex items-start justify-between">
          <div>
            <CardTitle>{r.name}</CardTitle>
            <CardDescription className="flex items-center gap-1 pt-1">
              <MapPin className="h-3 w-3" /> {r.city}
            </CardDescription>
          </div>
          <span className="inline-flex items-center gap-1 rounded-full border border-border bg-background px-2 py-0.5 text-xs font-medium text-foreground">
            <Star className="h-3 w-3 fill-yellow-400 text-yellow-400" /> {r.rating.toFixed(1)}
          </span>
        </div>
      </CardHeader>
      <CardContent className="flex-1 space-y-2 text-sm text-muted-foreground">
        <p className="font-medium text-foreground">{r.cuisine}</p>
        <p>Average: {formatLKR(r.avg_price)} per person</p>
        <p>Open {r.opening_time}–{r.closing_time}</p>
      </CardContent>
      <CardFooter className="flex gap-2">
        <Link href={`/restaurants/${r.id}`} className="flex-1"><Button variant="outline" className="w-full">View</Button></Link>
        <Link href={`/assistant?q=${encodeURIComponent(`Reserve a table at ${r.name}`)}`} className="flex-1">
          <Button className="w-full">Reserve</Button>
        </Link>
      </CardFooter>
    </Card>
  );
}