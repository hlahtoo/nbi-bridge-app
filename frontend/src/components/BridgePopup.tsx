import { useState } from "react";
import { Map } from "leaflet";
import { Bridge, BridgeDetail } from "@/types/types";

type BridgePopupProps = {
  bridge: Bridge;
  map: Map | null;
};

export default function BridgePopup({ bridge, map }: BridgePopupProps) {
  const [showMore, setShowMore] = useState(false);
  const [loading, setLoading] = useState(false);
  const [detailedData, setDetailedData] = useState<BridgeDetail | null>(null);

  const zoomToBridgeStep = () => {
    if (!map) return;
    const currentZoom = map.getZoom();
    const newZoom = Math.min(currentZoom + 1, 18);
    map.setView([bridge.lat_016, bridge.long_017], newZoom, { animate: true });
  };

  const fetchDetail = async () => {
    setLoading(true);
    try {
      const res = await fetch(
        `http://localhost:8000/api/bridges/detail/${bridge.structure_number_008}`
      );
      if (!res.ok) throw new Error("Failed to load detail");
      const data = await res.json();
      setDetailedData(data);
      setShowMore(true);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const Row = ({
    label,
    value,
  }: {
    label: string;
    value: string | number | undefined;
  }) => (
    <div className="flex flex-col">
      <span className="text-xs font-medium text-gray-500">{label}</span>
      <span className="text-sm text-gray-900 break-words">
        {value ?? "N/A"}
      </span>
    </div>
  );

  return (
    <div className="w-72 max-h-96 flex flex-col text-sm text-gray-700">
      {/* Title */}
      <div className="border-b px-3 pb-2 pt-3">
        <h2 className="text-xl font-semibold text-gray-800">Bridge Details</h2>
      </div>

      {/* Scrollable Content */}
      <div className="flex-1 overflow-y-auto px-3 py-2 space-y-3">
        <div className="grid grid-cols-2 gap-x-2 gap-y-1">
          <Row label="Structure #" value={bridge.structure_number_008} />
          <Row label="Latitude" value={bridge.lat_016} />
          <Row label="Longitude" value={bridge.long_017} />
          <Row label="Year Built" value={bridge.year_built_027} />
          <Row label="ADT" value={bridge.adt_029} />
          <Row label="Deck Cond." value={bridge.deck_cond_058} />
          <Row label="Superstructure" value={bridge.superstructure_cond_059} />
          <Row label="Substructure" value={bridge.substructure_cond_060} />
          <Row label="Channel Cond." value={bridge.channel_cond_061} />
          <Row label="Culvert Cond." value={bridge.culvert_cond_062} />
          <Row label="Reconstructed" value={bridge.year_reconstructed_106} />
          <Row label="Bridge Cond." value={bridge.bridge_condition} />
          <Row label="Lowest Rating" value={bridge.lowest_rating} />
          <Row
            label="Deck Area"
            value={bridge.deck_area ? `${bridge.deck_area} m²` : "N/A"}
          />
        </div>

        {showMore && detailedData && (
          <>
            <div className="grid grid-cols-2 gap-x-2 gap-y-1">
              {Object.entries(detailedData).map(([key, value]) => {
                // Skip values already rendered above
                const excludedKeys = [
                  "structure_number_008",
                  "state_code_001",
                  "lat_016",
                  "long_017",
                  "year_built_027",
                  "adt_029",
                  "deck_cond_058",
                  "superstructure_cond_059",
                  "substructure_cond_060",
                  "channel_cond_061",
                  "culvert_cond_062",
                  "year_reconstructed_106",
                  "bridge_condition",
                  "lowest_rating",
                  "deck_area",
                ];
                if (excludedKeys.includes(key)) return null;

                // Optional: friendly label overrides
                const labelMap: Record<string, string> = {
                  facility_carried_007: "Facility Carried",
                  features_desc_006a: "Features Desc.",
                  critical_facility_006b: "Critical Facility",
                  date_of_inspect_090: "Inspection Date",
                  scour_critical_113: "Scour Critical",
                  traffic_direction_102: "Traffic Direction",
                  deck_structure_type_107: "Deck Structure Type",
                  surface_type_108a: "Surface Type",
                  total_imp_cost_096: "Total Improvement Cost",
                  operating_rating_064: "Operating Rating",
                  inventory_rating_066: "Inventory Rating",
                };

                const label =
                  labelMap[key] ||
                  key
                    .replace(/_\d+[a-z]*$/i, "") // Remove trailing codes like _006a
                    .replace(/_/g, " ") // Replace underscores with spaces
                    .replace(/\b\w/g, (c) => c.toUpperCase()); // Capitalize each word

                return <Row key={key} label={label} value={value} />;
              })}
            </div>
          </>
        )}
      </div>

      {/* Fixed Footer Buttons */}
      <div className="flex justify-between px-3 py-2 border-t bg-white">
        <button
          onClick={zoomToBridgeStep}
          className="text-blue-600 hover:underline text-sm"
        >
          Zoom In
        </button>
        {!showMore && (
          <button
            onClick={fetchDetail}
            className="text-blue-600 hover:underline text-sm"
            disabled={loading}
          >
            {loading ? "Loading..." : "View Details"}
          </button>
        )}
      </div>
    </div>
  );
}
