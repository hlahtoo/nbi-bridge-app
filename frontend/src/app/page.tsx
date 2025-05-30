// Client-side rendered homepage that displays the interactive bridge map
"use client";

import dynamic from "next/dynamic";

// Dynamically import MapView component with SSR disabled (only render on client side)
const MapView = dynamic(() => import("../components/MapView"), { ssr: false });

export default function HomePage() {
  return (
    <main>
      {/* Page title */}
      <h1 className="text-xl font-bold p-4">Bridge Map Viewer</h1>

      {/* Interactive map component */}
      <MapView />
    </main>
  );
}
