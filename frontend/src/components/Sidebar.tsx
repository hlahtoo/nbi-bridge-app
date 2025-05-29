"use client";

import { Dispatch, SetStateAction } from "react";

export type Operator = ">=" | "<=";

export type SidebarProps = {
  mainFilter: string;
  setMainFilter: Dispatch<SetStateAction<string>>;
  limit: number;
  setLimit: Dispatch<SetStateAction<number>>;

  yearFilter: number | null;
  setYearFilter: Dispatch<SetStateAction<number | null>>;
  yearOp: Operator;
  setYearOp: Dispatch<SetStateAction<Operator>>;

  lowestRating: number | null;
  setLowestRating: Dispatch<SetStateAction<number | null>>;
  lowestRatingOp: Operator;
  setLowestRatingOp: Dispatch<SetStateAction<Operator>>;

  deckArea: number | null;
  setDeckArea: Dispatch<SetStateAction<number | null>>;
  deckAreaOp: Operator;
  setDeckAreaOp: Dispatch<SetStateAction<Operator>>;

  adt: number | null;
  setAdt: Dispatch<SetStateAction<number | null>>;
  adtOp: Operator;
  setAdtOp: Dispatch<SetStateAction<Operator>>;
};

function FilterInput({
  label,
  value,
  setValue,
  op,
  setOp,
}: {
  label: string;
  value: number | null;
  setValue: Dispatch<SetStateAction<number | null>>;
  op: Operator;
  setOp: Dispatch<SetStateAction<Operator>>;
}) {
  return (
    <div className="mb-4">
      <label className="block mb-1 font-medium text-black text-sm">
        {label}
      </label>
      <div className="flex gap-2">
        <select
          value={op}
          onChange={(e) => setOp(e.target.value as Operator)}
          className="border rounded px-2 text-sm"
        >
          <option value=">=">&ge;</option>
          <option value="<=">&le;</option>
        </select>
        <input
          type="number"
          value={value ?? ""}
          onChange={(e) =>
            setValue(e.target.value ? parseInt(e.target.value) : null)
          }
          className="w-full p-2 border rounded text-sm"
        />
      </div>
    </div>
  );
}

export default function Sidebar(props: SidebarProps) {
  return (
    <div className="w-64 bg-white shadow-lg p-4 overflow-y-auto h-full text-black">
      <h2 className="text-lg font-bold mb-4">Main Filter</h2>

      <div className="mb-4">
        <select
          value={props.mainFilter}
          onChange={(e) => props.setMainFilter(e.target.value)}
          className="w-full p-2 border rounded text-sm mb-2"
        >
          <option value="lowestRating">Lowest Rating</option>
          <option value="worstBridgeCondition">Worst Bridge Condition</option>
          <option value="highestADT">Highest ADT</option>
        </select>

        <div className="mb-4">
          <label className="block mb-1 font-medium text-black text-sm">
            Limit per Zoom-based Tile
          </label>
          <select
            value={props.limit}
            onChange={(e) => props.setLimit(parseInt(e.target.value))}
            disabled={props.mainFilter === "all"}
            className={`w-full p-2 border rounded text-sm ${
              props.mainFilter === "all"
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

      <h2 className="text-lg font-bold mb-4">Sub-Filters</h2>

      <FilterInput
        label="Year Built"
        value={props.yearFilter}
        setValue={props.setYearFilter}
        op={props.yearOp}
        setOp={props.setYearOp}
      />
      <FilterInput
        label="Lowest Rating"
        value={props.lowestRating}
        setValue={props.setLowestRating}
        op={props.lowestRatingOp}
        setOp={props.setLowestRatingOp}
      />
      <FilterInput
        label="Deck Area (m²)"
        value={props.deckArea}
        setValue={props.setDeckArea}
        op={props.deckAreaOp}
        setOp={props.setDeckAreaOp}
      />
      <FilterInput
        label="ADT (Daily Traffic)"
        value={props.adt}
        setValue={props.setAdt}
        op={props.adtOp}
        setOp={props.setAdtOp}
      />

      <button
        onClick={() => {
          props.setYearFilter(null);
          props.setLowestRating(null);
          props.setDeckArea(null);
          props.setAdt(null);
        }}
        className="text-blue-600 text-sm underline mt-2"
      >
        Clear Sub-Filters
      </button>
    </div>
  );
}
