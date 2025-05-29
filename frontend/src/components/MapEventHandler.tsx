"use client";
import { useEffect } from "react";
import { useMap } from "react-leaflet";

export default function MapEventHandler({
  onMoveEnd,
}: {
  onMoveEnd: (map: L.Map) => void;
}) {
  const map = useMap();

  useEffect(() => {
    const handleMoveEnd = () => onMoveEnd(map);

    // 🔥 Trigger manually once when map is ready
    map.whenReady(() => {
      onMoveEnd(map); // Initial fetch on load
      map.on("moveend", handleMoveEnd);
    });

    return () => {
      map.off("moveend", handleMoveEnd);
    };
  }, [map, onMoveEnd]);

  return null;
}
