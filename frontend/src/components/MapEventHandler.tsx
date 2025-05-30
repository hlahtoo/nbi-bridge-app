// MapEventHandler sets up a listener to call `onMoveEnd` whenever the user finishes panning or zooming the map.
// It also triggers an initial fetch once the map is ready.
"use client";
import { useEffect } from "react";
import { useMap } from "react-leaflet";

export default function MapEventHandler({
  onMoveEnd,
}: {
  onMoveEnd: (map: L.Map) => void;
}) {
  // Get access to the Leaflet map instance
  const map = useMap();

  useEffect(() => {
    // Wrapper function to pass map to the onMoveEnd callback
    const handleMoveEnd = () => onMoveEnd(map);

    // When the map is ready, trigger an initial data fetch and bind the "moveend" event
    map.whenReady(() => {
      onMoveEnd(map); // Initial fetch on load
      map.on("moveend", handleMoveEnd);
    });

    // Cleanup on unmount: remove the event listener
    return () => {
      map.off("moveend", handleMoveEnd);
    };
  }, [map, onMoveEnd]);

  // This component renders nothing in the UI, it's purely functional
  return null;
}
