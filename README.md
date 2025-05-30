# NBI Bridge Viewer

NBI Bridge Viewer is a full-stack geospatial web application that visualizes bridges from the National Bridge Inventory (NBI) dataset on an interactive map. It enables users to explore bridge infrastructure across the U.S., filter based on condition, traffic, or location, and fetch details using spatial tile-based queries for optimal performance.

## Features

- Interactive Leaflet map with real-time tile-based bridge loading
- FastAPI backend with spatial filtering via PostGIS
- PostgreSQL + PostGIS for geospatial querying
- Filter bridges by ADT (Average Daily Traffic), condition, or year
- View detailed bridge attributes (deck, superstructure, substructure conditions, etc.)
- Optimized tile caching for frontend to avoid redundant fetching
- Typed and schema-validated API using Pydantic

## Demo Screenshots

Below are some visuals of the working application, showcasing its major features.

### Bridge Map View

Displays bridges as markers on a Leaflet map. Users can pan and zoom to fetch bridges dynamically based on their view.

![Bridge Map View](https://firebasestorage.googleapis.com/v0/b/commit-genie.firebasestorage.app/o/Bridge-app%2FScreenshot%202025-05-29%20at%202.49.07%E2%80%AFAM.png?alt=media&token=4a5e48eb-8247-4fdf-ba02-abf9d4129da2)

---

### Bridge Detail Popup

Clicking a bridge marker brings up a detailed popup showing condition ratings, year built, and other metadata.

![Bridge Detail](https://firebasestorage.googleapis.com/v0/b/commit-genie.firebasestorage.app/o/Bridge-app%2FScreenshot%202025-05-29%20at%202.49.34%E2%80%AFAM.png?alt=media&token=1dbf256c-e357-4bcc-a5b6-c91d3e81e993)

## Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/yourname/nbi-bridge-viewer.git
cd nbi-bridge-viewer
```

---

### 2. Backend Setup (FastAPI)

#### Install dependencies:

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Set up `.env` file:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/bridges
```

#### Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

> App will be live at: `http://localhost:8000`

---

### 3. Frontend Setup (Next.js)

#### Install dependencies:

```bash
cd frontend
npm install
```

#### Run development server:

```bash
npm run dev
```

> Frontend will run at: `http://localhost:3000`

## API Overview

This project provides a FastAPI-based backend to retrieve and explore data from the National Bridge Inventory. It exposes several endpoints for querying bridges based on tiles, zoom levels, and filters, as well as viewing detailed bridge information.

### Base URL

```
/api/bridges
```

---

### ### `GET /api/bridges`

**Description:**  
Fetches a list of bridge records from the `bridge_core` table.

**Query Parameters:**

| Name  | Type | Description                                          |
| ----- | ---- | ---------------------------------------------------- |
| limit | int  | (Optional) Number of bridges to fetch (default: 100) |

**Response:**  
Returns a list of simplified bridge data including coordinates, ADT, and condition ratings.

---

### ### `POST /api/bridges/batch`

**Description:**  
Fetches bridges using a tile-based spatial filter. Supports two modes: `batch` (merged area) and `single` (one bridge per tile).

**Body:**

```json
{
  "tiles": [[x1, y1], [x2, y2], ...],
  "zoom": 10
}
```

**Query Parameters:**

| Name      | Type | Description                                                        |
| --------- | ---- | ------------------------------------------------------------------ |
| limit     | int  | Maximum number of records to return (default: 100)                 |
| filterKey | str  | Sorting mode: `default`, `lowestRating`, or `highestADT`           |
| mode      | str  | Tile mode: `batch` (union of all tiles) or `single` (top per tile) |

**Modes:**

- **Batch mode:** Combines tiles using `ST_Union` and returns bridges intersecting that area.
- **Single mode:** Picks top `n` bridges from each tile based on `filterKey`.

**Response:**  
List of filtered bridges based on spatial queries and filters.

---

### ### `GET /api/bridges/detail/{structure_number}`

**Description:**  
Fetches full detail for a specific bridge from the `bridge_details` table.

**Path Parameters:**

| Name             | Type   | Description                     |
| ---------------- | ------ | ------------------------------- |
| structure_number | string | Unique identifier of the bridge |

**Response:**  
Detailed bridge data including:

- State code
- Location coordinates
- Year built and reconstructed
- Ratings for deck, superstructure, substructure, and channel
- ADT (Average Daily Traffic)
- Deck area and lowest rating

**Errors:**

- `404 Not Found`: If the specified bridge does not exist

---

### Data Sources

- `bridge_core`: Lightweight reference data used in tile-based queries
- `bridge_details`: Full bridge details for individual queries

## Frontend Overview

The frontend is built using **React** and **Leaflet**, offering an interactive map interface that dynamically fetches and renders bridge data. The design emphasizes usability and performance, with spatial filtering based on map movement and zoom.

---

### Key Features

#### Tile-Based Map with Caching

- The map automatically detects which tile areas (based on zoom and viewport) are visible using a `latLngToTile` conversion.
- Efficient caching is implemented using a `tileCache` keyed by tile+filter combo to prevent redundant API calls.
- Only newly visible tiles are requested when the user pans or zooms.

#### Bridge Condition Filtering

- Users can view bridges sorted by different metrics via `filterKey`:
  - `default`: Uses overall bridge condition
  - `lowestRating`: Sorts by structural deficiency
  - `highestADT`: Shows bridges with highest traffic load
- These filters determine sort order on the backend and are part of cache keying logic.

#### Batch vs Single Mode Queries

- **Batch mode:** Union of all visible tiles, returns bridges intersecting the entire region.
- **Single mode:** Ensures each tile gets at least one top-rated bridge, helping evenly distribute results across the map.

#### Interactive Map Clicks

- Clicking on a bridge pin (marker) opens a modal or popup with high-level details.
- These include location, condition ratings, and traffic stats.

#### Auto Update on Map Move

- When the user pans or zooms:
  1. The frontend calculates the new visible tile keys.
  2. It filters out already fetched ones using the cache.
  3. It sends only new tiles to the backend for fresh data.
