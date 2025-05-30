"""
Tile-based spatial query utilities for fetching bridge data using bounding boxes and spatial filters.
"""
from math import atan, exp, pi
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.bridge import TileBatchRequest

def tile_to_bbox(tileX: int, tileY: int, zoom: int):
    """
    Convert XYZ tile coordinates to latitude/longitude bounding box.
    """
    # Total number of tiles across the world at this zoom level
    n = 2 ** zoom
    
    # Convert X tile index to longitude range
    # Tiles start at -180° longitude (left edge of the world map)
    # Each tile spans (360 / n) degrees of longitude
    lon_min = tileX / n * 360.0 - 180.0
    lon_max = (tileX + 1) / n * 360.0 - 180.0

    # Convert Y tile index to latitude range using inverse of Mercator projection
    
    # First compute the radian value corresponding to the top edge (max latitude)
    # Formula: lat_rad = π * (1 - 2 * tileY / n)
    # Then convert from radians to degrees using: latitude = 180/π * (2 * atan(exp(lat_rad)) - π/2)
    lat_rad_max = pi * (1 - 2 * tileY / n)
    lat_max = 180 / pi * (2 * atan(exp(lat_rad_max)) - pi / 2)

    # Do the same for the bottom edge (min latitude), which is tileY + 1
    lat_rad_min = pi * (1 - 2 * (tileY + 1) / n)
    lat_min = 180 / pi * (2 * atan(exp(lat_rad_min)) - pi / 2)

    # Return the bounding box: [south, north, west, east]
    return lat_min, lat_max, lon_min, lon_max


def single_tile_query(req: TileBatchRequest, limit: int, order_clause: str, db: Session):
    """
    Return top N bridges per tile using spatial intersection and partitioned row number.
    """
    cases = []
    params = {}

    # Generate SQL CASE WHEN clauses for each tile
    for i, (x, y) in enumerate(req.tiles):
        lat_min, lat_max, lon_min, lon_max = tile_to_bbox(x, y, req.zoom)
        params.update({
            f"lat{i}a": lat_min, f"lat{i}b": lat_max,
            f"lon{i}a": lon_min, f"lon{i}b": lon_max
        })
        cases.append(
            f"""
            WHEN ST_Intersects(geom, ST_MakeEnvelope(:lon{i}a, :lat{i}a, :lon{i}b, :lat{i}b, 4326))
            THEN 'tile_{i}'
            """
        )

    # Create tile_id column from spatial conditions
    case_sql = "CASE " + " ".join(cases) + " END AS tile_id"

    # SQL with partitioned row_number to get top N bridges per tile
    sql = f"""
    WITH per_tile_limited AS (
        SELECT *,
               ROW_NUMBER() OVER (
                 PARTITION BY tile_id
                 ORDER BY {order_clause}
               ) AS rn
        FROM (
            SELECT *,
                   {case_sql}
            FROM bridge_core
        ) sub
    )
    SELECT *
    FROM per_tile_limited
    WHERE rn <= :limit;
    """
    params["limit"] = limit
    return db.execute(text(sql), params).mappings().all()


def batch_tile_query(req: TileBatchRequest, limit: int, order_clause: str, db: Session):
    """
    Return top N bridges from the union of all tiles using spatial intersection.
    """    
    envelopes = []
    
    # Convert each tile to an envelope bounding box
    for x, y in req.tiles:
        lat_min, lat_max, lon_min, lon_max = tile_to_bbox(x, y, req.zoom)
        envelopes.append(f"ST_MakeEnvelope({lon_min}, {lat_min}, {lon_max}, {lat_max}, 4326)")

    # Create union of all tile geometries
    union = "ST_Union(ARRAY[" + ", ".join(envelopes) + "])"

    # SQL query to fetch bridges intersecting the unioned area
    sql = f"""
        SELECT 
            structure_number_008,
            state_code_001,
            lat_016,
            long_017,
            year_built_027,
            adt_029,
            deck_cond_058,
            superstructure_cond_059,
            substructure_cond_060,
            channel_cond_061,
            culvert_cond_062,
            year_reconstructed_106,
            bridge_condition,
            lowest_rating,
            deck_area
        FROM bridge_core
        WHERE ST_Intersects(geom, {union})
        ORDER BY {order_clause}
        LIMIT :limit;
    """
    return db.execute(text(sql), {"limit": limit}).mappings().all()