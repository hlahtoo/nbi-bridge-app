"use client";

import dynamic from "next/dynamic";

const MapView = dynamic(() => import("../components/MapView"), { ssr: false });

export default function HomePage() {
  return (
    <main>
      <h1 className="text-xl font-bold p-4">Bridge Map Viewer</h1>
      <MapView />
    </main>
  );
}
