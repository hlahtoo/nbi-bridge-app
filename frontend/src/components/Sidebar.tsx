// Sidebar component for controlling bridge filters in the map viewer
"use client";

import { Dispatch, SetStateAction } from "react";

// Operator type used for comparisons in filter inputs
export type Operator = ">=" | "<=";

// Filters object tracks all active filters in the sidebar
export type Filters = {
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
};

// Props passed to the Sidebar component
export type SidebarProps = {
  filters: Filters;
  setFilters: Dispatch<SetStateAction<Filters>>;
};

// Reusable input + operator component for numeric filters
function FilterInput({
  label,
  valueKey,
  opKey,
  filters,
  setFilters,
}: {
  label: string;
  valueKey: keyof Filters;
  opKey: keyof Filters;
  filters: Filters;
  setFilters: Dispatch<SetStateAction<Filters>>;
}) {
  return (
    <div className="mb-4">
      <label className="block mb-1 font-medium text-black text-sm">
        {label}
      </label>
      <div className="flex gap-2">
        {/* Operator selector (>= or <=) */}
        <select
          value={filters[opKey] as Operator}
          onChange={(e) =>
            setFilters((prev) => ({
              ...prev,
              [opKey]: e.target.value as Operator,
            }))
          }
          className="border rounded px-2 text-sm"
        >
          <option value=">=">&ge;</option>
          <option value="<=">&le;</option>
        </select>

        {/* Numeric input field */}
        <input
          type="number"
          value={filters[valueKey] ?? ""}
          onChange={(e) =>
            setFilters((prev) => ({
              ...prev,
              [valueKey]: e.target.value ? parseInt(e.target.value) : null,
            }))
          }
          className="w-full p-2 border rounded text-sm"
        />
      </div>
    </div>
  );
}

// Sidebar component for adjusting bridge filters and view settings
export default function Sidebar({ filters, setFilters }: SidebarProps) {
  return (
    <div className="w-64 bg-white shadow-lg p-4 overflow-y-auto h-full text-black">
      {/* Main filtering section */}
      <h2 className="text-lg font-bold mb-4">Main Filter</h2>

      <div className="mb-4">
        {/* Main filter dropdown (sorting mode) */}
        <select
          value={filters.mainFilter}
          onChange={(e) =>
            setFilters((prev) => ({ ...prev, mainFilter: e.target.value }))
          }
          className="w-full p-2 border rounded text-sm mb-2"
        >
          <option value="lowestRating">Lowest Rating</option>
          <option value="worstBridgeCondition">Worst Bridge Condition</option>
          <option value="highestADT">Highest ADT</option>
        </select>

        {/* Limit dropdown (how many bridges per tile) */}
        <div className="mb-4">
          <label className="block mb-1 font-medium text-black text-sm">
            Limit per Zoom-based Tile
          </label>
          <select
            value={filters.limit}
            onChange={(e) =>
              setFilters((prev) => ({
                ...prev,
                limit: parseInt(e.target.value),
              }))
            }
            disabled={filters.mainFilter === "all"}
            className={`w-full p-2 border rounded text-sm ${
              filters.mainFilter === "all"
                ? "bg-gray-200 cursor-not-allowed text-gray-500"
                : ""
            }`}
          >
            {[10, 20, 50, 100, 500].map((limit) => (
              <option key={limit} value={limit}>
                {limit}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Sub-filters for numeric fields */}
      <h2 className="text-lg font-bold mb-4">Sub-Filters</h2>

      <FilterInput
        label="Year Built"
        valueKey="yearFilter"
        opKey="yearOp"
        filters={filters}
        setFilters={setFilters}
      />
      <FilterInput
        label="Lowest Rating"
        valueKey="lowestRating"
        opKey="lowestRatingOp"
        filters={filters}
        setFilters={setFilters}
      />
      <FilterInput
        label="Deck Area (m²)"
        valueKey="deckArea"
        opKey="deckAreaOp"
        filters={filters}
        setFilters={setFilters}
      />
      <FilterInput
        label="ADT (Daily Traffic)"
        valueKey="adt"
        opKey="adtOp"
        filters={filters}
        setFilters={setFilters}
      />

      {/* Button to clear and reset all sub-filters */}
      <button
        onClick={() =>
          setFilters((prev) => ({
            ...prev,
            yearFilter: null,
            lowestRating: null,
            deckArea: null,
            adt: null,
          }))
        }
        className="text-blue-600 text-sm underline mt-2"
      >
        Clear Sub-Filters
      </button>
    </div>
  );
}
