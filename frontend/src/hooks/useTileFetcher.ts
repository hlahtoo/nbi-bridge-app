// useTileFetcher: Custom hook that fetches bridge data by tile on map move, with caching
"use client";

import { useRef, useState } from "react";

import { Bridge } from "@/types/types";
import L from "leaflet";

// Convert latitude/longitude to tile X/Y at a specific zoom level
function latLngToTile(lat: number, lng: number, zoom: number) {
  const n = 2 ** zoom;
  const x = Math.floor(((lng + 180) / 360) * n);
  const y = Math.floor(
    ((1 -
      Math.log(
        Math.tan((lat * Math.PI) / 180) + 1 / Math.cos((lat * Math.PI) / 180)
      ) /
        Math.PI) /
      2) *
      n
  );
  return { x, y };
}

// Generate all tile keys (e.g. "12_654_1583") for current map bounds and zoom
function getTileKeys(map: L.Map, zoom: number) {
  const bounds = map.getBounds();
  const sw = bounds.getSouthWest();
  const ne = bounds.getNorthEast();

  const { x: x1, y: y1 } = latLngToTile(sw.lat, sw.lng, zoom);
  const { x: x2, y: y2 } = latLngToTile(ne.lat, ne.lng, zoom);

  const keys: string[] = [];
  for (let x = x1; x <= x2; x++) {
    for (let y = Math.min(y1, y2); y <= Math.max(y1, y2); y++) {
      keys.push(`${zoom}_${x}_${y}`);
    }
  }

  return keys;
}

// Hook for tile-based bridge data fetching with caching
export function useTileFetcher({
  mainFilter,
  limit,
  fetchFromBackend,
  setBridges,
}: {
  mainFilter: string;
  limit: number;
  fetchFromBackend: (
    zoom: number,
    tileKeys: string[],
    filterKey: string
  ) => Promise<Bridge[]>;
  setBridges: React.Dispatch<React.SetStateAction<Bridge[]>>;
}) {
  // Cache of already fetched tile keys to avoid duplicate requests
  const tileCache = useRef<Record<string, Set<string>>>({});

  // Clears all cached tiles (useful when filter changes)
  const clearCache = () => {
    tileCache.current = {};
  };

  // Ref to store the Leaflet map instance
  const mapRef = useRef<L.Map | null>(null);

  // Called when map movement ends (zoom or pan)
  const onMoveEnd = async (map: L.Map) => {
    const zoom = map.getZoom();
    const filterKey = mainFilter;

    const tileKeys = getTileKeys(map, zoom);

    // Ensure filterKey exists in cache map
    if (!tileCache.current[filterKey]) {
      tileCache.current[filterKey] = new Set();
    }

    // Filter out already fetched tiles
    const newTileKeys: string[] = [];

    for (const tileKey of tileKeys) {
      if (!tileCache.current[filterKey].has(tileKey)) {
        newTileKeys.push(tileKey);
        tileCache.current[filterKey].add(tileKey);
      }
    }

    // If all tiles are cached, skip fetch
    if (newTileKeys.length === 0) return;

    // Fetch bridge data for new tiles
    const newBridges = await fetchFromBackend(zoom, newTileKeys, filterKey);

    // Merge new data while avoiding duplicates
    setBridges((prev) => {
      const seen = new Set(prev.map((b) => b.structure_number_008));
      return [
        ...prev,
        ...newBridges.filter((b) => !seen.has(b.structure_number_008)),
      ];
    });
  };

  return {
    mapRef,
    onMoveEnd,
    clearCache,
  };
}
