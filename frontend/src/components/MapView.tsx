// Client-side rendered map view that fetches and filters NBI bridge data using tile-based spatial queries
"use client";

import { useState, useEffect, useRef, useMemo } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { LatLngExpression } from "leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import Sidebar from "./Sidebar";
import { useTileFetcher } from "../hooks/useTileFetcher";
import BridgePopup from "./BridgePopup";
import MapEventHandler from "./MapEventHandler";
delete (L.Icon.Default.prototype as any)._getIconUrl;

// Fix Leaflet icon path issues in Next.js
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "/leaflet/marker-icon-2x.png",
  iconUrl: "/leaflet/marker-icon.png",
  shadowUrl: "/leaflet/marker-shadow.png",
});
import { Bridge } from "@/types/types";

export default function MapView() {
  // Default map center (for Pennsylvania)
  const center: LatLngExpression = [41.2033, -77.1945];
  type Operator = ">=" | "<=";

  // UI filter state
  const [filters, setFilters] = useState<{
    mainFilter: string;
    limit: number;
    yearFilter: number | null;
    yearOp: Operator;
    lowestRating: number | null;
    lowestRatingOp: Operator;
    deckArea: number | null;
    deckAreaOp: Operator;
    adt: number | null;
    adtOp: Operator;
  }>({
    mainFilter: "lowestRating",
    limit: 50,
    yearFilter: null,
    yearOp: ">=",
    lowestRating: null,
    lowestRatingOp: ">=",
    deckArea: null,
    deckAreaOp: ">=",
    adt: null,
    adtOp: ">=",
  });

  // List of bridges to display
  const [bridges, setBridges] = useState<Bridge[]>([]);

  // Re-fetch bridges whenever filter changes
  useEffect(() => {
    setBridges([]);
    clearCache();
    if (mapRef.current) {
      mapRef.current.fire("moveend");
    }
  }, [filters.mainFilter, filters.limit]);

  // Tile fetcher hook handles spatial fetching logic
  const { mapRef, onMoveEnd, clearCache } = useTileFetcher({
    mainFilter: filters.mainFilter,
    limit: filters.limit,

    // Backend tile fetch function triggered by map movement or zoom level changes
    fetchFromBackend: async (zoom, tileKeys, filterKey) => {
      // Convert tileKeys like "tile_5_7" into [x, y] pairs
      const tiles = tileKeys.map((key) => {
        const [, x, y] = key.split("_").map(Number);
        return [x, y];
      });

      /**
       * Determine which query mode to use:
       * - "single" mode (zoom < 10): fewer tiles, broader region, fewer bridges per tile.
       *   Fetches top N bridges globally across the tiles (used for performance at low zoom).
       * - "batch" mode (zoom >= 10): more tiles, finer detail.
       *   Fetches top N bridges per tile (for more granular control).
       */
      const mode = zoom < 10 ? "single" : "batch";

      // Fetch bridge data from backend using selected mode and filters
      const res = await fetch(
        `http://localhost:8000/api/bridges/batch?zoom=${zoom}&filterKey=${filterKey}&limit=${filters.limit}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ tiles, zoom, mode }),
        }
      );

      if (!res.ok) {
        console.error("❌ Failed to fetch bridges");
        return [];
      }

      const bridges = await res.json();
      return bridges;
    },

    // Callback to update global bridge state when new data is loaded
    setBridges,
  });

  // Memoize the filtered bridge list to avoid unnecessary recalculations on every render

  const finalFiltered = useMemo(() => {
    // Helper function to compare a bridge field value to the user's filter input.
    const compare = (
      value: number | undefined,
      target: number | null,
      op: Operator
    ) => {
      if (target === null || value === undefined) return true;
      return op === ">=" ? value >= target : value <= target;
    };

    // Filter bridge list based on active sub-filters:
    return bridges.filter(
      (b) =>
        compare(b.year_built_027, filters.yearFilter, filters.yearOp) &&
        compare(
          b.lowest_rating,
          filters.lowestRating,
          filters.lowestRatingOp
        ) &&
        compare(b.deck_area, filters.deckArea, filters.deckAreaOp) &&
        compare(b.adt_029, filters.adt, filters.adtOp)
    );
  }, [bridges, filters]); // useMemo dependencies: re-run only when bridges or filters change

  // Initial fetch when map is ready
  useEffect(() => {
    if (!mapRef.current) return;

    mapRef.current.whenReady(() => {
      onMoveEnd(mapRef.current!);
    });
  }, [mapRef]);

  return (
    <div className="flex h-screen">
      {/* Sidebar UI with filters */}
      <Sidebar filters={filters} setFilters={setFilters} />

      {/* Leaflet Map Container */}
      <div className="flex-1">
        <MapContainer
          center={center}
          zoom={9}
          style={{ height: "100%", width: "100%" }}
          ref={mapRef}
        >
          {/* Base tile layer */}
          <TileLayer
            attribution="&copy; OpenStreetMap contributors"
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {/* Custom map movement handler */}
          <MapEventHandler onMoveEnd={onMoveEnd} />

          {/* Render filtered bridge markers */}
          {finalFiltered.map((bridge, i) => (
            <Marker key={i} position={[bridge.lat_016, bridge.long_017]}>
              <Popup>
                <BridgePopup bridge={bridge} map={mapRef.current} />
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
}
