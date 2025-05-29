"use client";

import { useState, useEffect, useRef } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { LatLngExpression } from "leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import Sidebar from "./Sidebar";
import { useTileFetcher } from "../hooks/useTileFetcher";
import BridgePopup from "./BridgePopup";
import MapEventHandler from "./MapEventHandler";
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "/leaflet/marker-icon-2x.png",
  iconUrl: "/leaflet/marker-icon.png",
  shadowUrl: "/leaflet/marker-shadow.png",
});
import { Bridge } from "@/types/types";

export default function MapView() {
  const center: LatLngExpression = [41.2033, -77.1945];
  type Operator = ">=" | "<=";

  const [mainFilter, setMainFilter] = useState("lowestRating");
  const [limit, setLimit] = useState(100);
  const [yearFilter, setYearFilter] = useState<number | null>(null);
  const [yearOp, setYearOp] = useState<Operator>(">=");
  const [lowestRating, setLowestRating] = useState<number | null>(null);
  const [lowestRatingOp, setLowestRatingOp] = useState<Operator>(">=");
  const [deckArea, setDeckArea] = useState<number | null>(null);
  const [deckAreaOp, setDeckAreaOp] = useState<Operator>(">=");
  const [adt, setAdt] = useState<number | null>(null);
  const [adtOp, setAdtOp] = useState<Operator>(">=");

  const [bridges, setBridges] = useState<Bridge[]>([]);

  useEffect(() => {
    setBridges([]);
    clearCache();

    // Trigger re-fetch for current tiles
    if (mapRef.current) {
      mapRef.current.fire("moveend");
    }
  }, [mainFilter, limit]);

  const { mapRef, onMoveEnd, clearCache } = useTileFetcher({
    mainFilter,
    limit,
    fetchFromBackend: async (zoom, tileKeys, filterKey) => {
      console.log("Fetching for", filterKey, "at zoom", zoom);

      const tiles = tileKeys.map((key) => {
        const [, x, y] = key.split("_").map(Number);
        return [x, y];
      });

      const mode = zoom < 10 ? "single" : "batch";

      const res = await fetch(
        `http://localhost:8000/api/bridges/batch?zoom=${zoom}&filterKey=${filterKey}&limit=${limit}`,
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
    setBridges,
  });

  const compare = (
    value: number | undefined,
    target: number | null,
    op: Operator
  ) => {
    if (target === null || value === undefined) return true;
    return op === ">=" ? value >= target : value <= target;
  };

  const finalFiltered = bridges.filter((b) => {
    return (
      compare(b.year_built_027, yearFilter, yearOp) &&
      compare(b.lowest_rating, lowestRating, lowestRatingOp) &&
      compare(b.deck_area, deckArea, deckAreaOp) &&
      compare(b.adt_029, adt, adtOp)
    );
  });
  useEffect(() => {
    if (!mapRef.current) return;

    mapRef.current.whenReady(() => {
      onMoveEnd(mapRef.current!);
    });
  }, [mapRef]);

  return (
    <div className="flex h-screen">
      <Sidebar
        mainFilter={mainFilter}
        setMainFilter={setMainFilter}
        limit={limit}
        setLimit={setLimit}
        yearFilter={yearFilter}
        setYearFilter={setYearFilter}
        yearOp={yearOp}
        setYearOp={setYearOp}
        lowestRating={lowestRating}
        setLowestRating={setLowestRating}
        lowestRatingOp={lowestRatingOp}
        setLowestRatingOp={setLowestRatingOp}
        deckArea={deckArea}
        setDeckArea={setDeckArea}
        deckAreaOp={deckAreaOp}
        setDeckAreaOp={setDeckAreaOp}
        adt={adt}
        setAdt={setAdt}
        adtOp={adtOp}
        setAdtOp={setAdtOp}
      />
      <div className="flex-1">
        <MapContainer
          center={center}
          zoom={9}
          style={{ height: "100%", width: "100%" }}
          ref={mapRef}
        >
          <TileLayer
            attribution="&copy; OpenStreetMap contributors"
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <MapEventHandler onMoveEnd={onMoveEnd} />
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
