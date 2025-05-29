import { Bridge } from "./MapView";

type Props = {
  bridge: Bridge;
  onClose: () => void;
};

export default function BridgeDetailModal({ bridge, onClose }: Props) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm">
      <div className="relative w-full max-w-xl bg-white rounded-2xl shadow-xl p-6">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-3 right-4 text-gray-500 hover:text-gray-800 text-xl font-bold"
        >
          ×
        </button>

        {/* Title */}
        <h2 className="text-xl font-semibold text-gray-800 mb-4 border-b pb-2">
          Bridge Details
        </h2>

        {/* Detail Grid */}
        <div className="grid grid-cols-2 gap-x-4 gap-y-3 text-sm text-gray-700">
          <Detail label="Structure #" value={bridge.structure_number_008} />
          <Detail label="Latitude" value={bridge.lat_016} />
          <Detail label="Longitude" value={bridge.long_017} />
          <Detail label="Year Built" value={bridge.year_built_027} />
          <Detail label="ADT" value={bridge.adt_029} />
          <Detail label="Status" value={bridge.open_closed_posted_041} />
          <Detail label="Deck Cond." value={bridge.deck_cond_058} />
          <Detail label="Bridge Cond." value={bridge.bridge_condition} />
          <Detail label="Lowest Rating" value={bridge.lowest_rating} />
          <Detail
            label="Deck Area"
            value={bridge.deck_area ? `${bridge.deck_area} m²` : "N/A"}
          />
        </div>
      </div>
    </div>
  );
}

function Detail({
  label,
  value,
}: {
  label: string;
  value: string | number | undefined;
}) {
  return (
    <div className="flex flex-col">
      <span className="text-xs font-medium text-gray-500">{label}</span>
      <span className="text-sm text-gray-900 break-words">
        {value ?? "N/A"}
      </span>
    </div>
  );
}
