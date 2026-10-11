"use client";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { RestaurantCard } from "@/components/RestaurantCard";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useState } from "react";

const CUISINES = ["", "Italian", "Chinese", "Japanese", "Indian", "Sri Lankan", "Mexican", "Thai", "American"];

export default function RestaurantsPage() {
  const [q, setQ] = useState("");
  const [cuisine, setCuisine] = useState("");
  const [city, setCity] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [minRating, setMinRating] = useState("");
  const [sort, setSort] = useState("rating_desc");

  const { data, isLoading } = useQuery({
    queryKey: ["restaurants", q, cuisine, city, maxPrice, minRating, sort],
    queryFn: () => api.listRestaurants({ q, cuisine, city, max_price: maxPrice, min_rating: minRating, sort }),
  });

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Restaurants</h1>
      <div className="grid gap-3 md:grid-cols-6">
        <Input placeholder="Search name..." value={q} onChange={(e) => setQ(e.target.value)} />
        <select className="h-9 rounded-md border px-3 text-sm" value={cuisine} onChange={(e) => setCuisine(e.target.value)}>
          {CUISINES.map((c) => <option key={c} value={c}>{c || "Any cuisine"}</option>)}
        </select>
        <Input placeholder="City" value={city} onChange={(e) => setCity(e.target.value)} />
        <Input placeholder="Max price" type="number" value={maxPrice} onChange={(e) => setMaxPrice(e.target.value)} />
        <Input placeholder="Min rating" type="number" step="0.1" value={minRating} onChange={(e) => setMinRating(e.target.value)} />
        <select className="h-9 rounded-md border px-3 text-sm" value={sort} onChange={(e) => setSort(e.target.value)}>
          <option value="rating_desc">Rating ↓</option>
          <option value="price_asc">Price ↑</option>
          <option value="price_desc">Price ↓</option>
        </select>
      </div>

      {isLoading && <p>Loading...</p>}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {data?.items?.map((r: any) => <RestaurantCard key={r.id} r={r} />)}
      </div>
    </div>
  );
}