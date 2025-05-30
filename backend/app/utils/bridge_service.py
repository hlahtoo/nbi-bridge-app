from math import atan, exp, pi
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.bridge import TileBatchRequest

def tile_to_bbox(tileX: int, tileY: int, zoom: int):
    n = 2 ** zoom
    lon_min = tileX / n * 360.0 - 180.0
    lon_max = (tileX + 1) / n * 360.0 - 180.0

    lat_rad_max = pi * (1 - 2 * tileY / n)
    lat_max = 180 / pi * (2 * atan(exp(lat_rad_max)) - pi / 2)

    lat_rad_min = pi * (1 - 2 * (tileY + 1) / n)
    lat_min = 180 / pi * (2 * atan(exp(lat_rad_min)) - pi / 2)

    return lat_min, lat_max, lon_min, lon_max


def single_tile_query(req: TileBatchRequest, limit: int, order_clause: str, db: Session):
    cases = []
    params = {}

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

    case_sql = "CASE " + " ".join(cases) + " END AS tile_id"

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
    envelopes = []
    for x, y in req.tiles:
        lat_min, lat_max, lon_min, lon_max = tile_to_bbox(x, y, req.zoom)
        envelopes.append(f"ST_MakeEnvelope({lon_min}, {lat_min}, {lon_max}, {lat_max}, 4326)")

    union = "ST_Union(ARRAY[" + ", ".join(envelopes) + "])"

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