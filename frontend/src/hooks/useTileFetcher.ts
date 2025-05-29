"use client";

import { useRef, useState } from "react";

import { Bridge } from "@/types/types";
import L from "leaflet";

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

function getMainFilterKey(mainFilter: string, limit: number) {
  return `${mainFilter}_${limit}`;
}

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
  const tileCache = useRef<Record<string, Set<string>>>({});
  const fetchedAllOnce = useRef<boolean>(false); // <--- NEW
  const clearCache = () => {
    tileCache.current = {};
  };
  const mapRef = useRef<L.Map | null>(null);

  const onMoveEnd = async (map: L.Map) => {
    const zoom = map.getZoom();
    const filterKey = getMainFilterKey(mainFilter, limit);

    const tileKeys = getTileKeys(map, zoom);

    if (!tileCache.current[filterKey]) {
      tileCache.current[filterKey] = new Set();
    }

    const newTileKeys: string[] = [];

    for (const tileKey of tileKeys) {
      if (!tileCache.current[filterKey].has(tileKey)) {
        newTileKeys.push(tileKey);
        tileCache.current[filterKey].add(tileKey);
      }
    }

    if (newTileKeys.length === 0) return;

    const newBridges = await fetchFromBackend(zoom, newTileKeys, filterKey);

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
