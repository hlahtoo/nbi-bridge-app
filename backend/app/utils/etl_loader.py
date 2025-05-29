# app/db/load_data.py

import pandas as pd
from shapely.geometry import Point
from geoalchemy2.shape import from_shape
from sqlalchemy.orm import Session
from app.db.models import BridgeCore, BridgeDetails
from app.db.session import SessionLocal


def convert_dms_to_decimal(value: str, is_latitude=True) -> float:
    value = value.zfill(8 if is_latitude else 9)
    if is_latitude:
        deg = int(value[:2])
        minutes = int(value[2:4])
        seconds = float(value[4:])
    else:
        deg = int(value[:3])
        minutes = int(value[3:5])
        seconds = float(value[5:])
    decimal = deg + (minutes / 60) + (seconds / 3600)
    return round(decimal if is_latitude else -decimal, 6)


def load_bridges_from_txt(file_path: str):
    db = SessionLocal()
    df = pd.read_csv(file_path, dtype=str).fillna("")

    bridge_core_objs = []
    bridge_details_objs = []

    for _, row in df.iterrows():
        try:
            lat = convert_dms_to_decimal(row["LAT_016"]) if row["LAT_016"] else None
            lon = convert_dms_to_decimal(row["LONG_017"], is_latitude=False) if row["LONG_017"] else None
            geom = from_shape(Point(lon, lat), srid=4326) if lat and lon else None

            core = BridgeCore(
                structure_number_008=row["STRUCTURE_NUMBER_008"].strip(),
                state_code_001=row["STATE_CODE_001"],
                record_type_005a=row["RECORD_TYPE_005A"],
                route_prefix_005b=row["ROUTE_PREFIX_005B"],
                service_level_005c=row["SERVICE_LEVEL_005C"],

                location_009=row["LOCATION_009"],
                lat_016=lat,
                long_017=lon,
                geom=geom,
                maintenance_021=row["MAINTENANCE_021"],
                owner_022=row["OWNER_022"],
                functional_class_026=row["FUNCTIONAL_CLASS_026"],
                year_built_027=int(row["YEAR_BUILT_027"]) if row["YEAR_BUILT_027"].isdigit() else None,
                traffic_lanes_on_028a=int(row["TRAFFIC_LANES_ON_028A"]) if row["TRAFFIC_LANES_ON_028A"].isdigit() else None,
                traffic_lanes_und_028b=int(row["TRAFFIC_LANES_UND_028B"]) if row["TRAFFIC_LANES_UND_028B"].isdigit() else None,
                adt_029=int(row["ADT_029"]) if row["ADT_029"].isdigit() else None,
                
                design_load_031=row["DESIGN_LOAD_031"],

                structure_kind_043a=row["STRUCTURE_KIND_043A"],
                structure_type_043b=row["STRUCTURE_TYPE_043B"],
                deck_cond_058=row["DECK_COND_058"],
                superstructure_cond_059=row["SUPERSTRUCTURE_COND_059"],
                substructure_cond_060=row["SUBSTRUCTURE_COND_060"],
                channel_cond_061=row["CHANNEL_COND_061"],
                culvert_cond_062=row["CULVERT_COND_062"],

                year_reconstructed_106=int(row["YEAR_RECONSTRUCTED_106"]) if row["YEAR_RECONSTRUCTED_106"].isdigit() else None,
                bridge_condition=row["BRIDGE_CONDITION"],
                lowest_rating=int(row["LOWEST_RATING"]) if row["LOWEST_RATING"].isdigit() else None,
                deck_area=float(row["DECK_AREA"]) if row["DECK_AREA"] else None,

            )

            details = BridgeDetails(
                structure_number_008=row["STRUCTURE_NUMBER_008"].strip(),
                features_desc_006a=row["FEATURES_DESC_006A"],
                route_number_005d=row["ROUTE_NUMBER_005D"],
                direction_005e=row["DIRECTION_005E"],
                highway_district_002=row["HIGHWAY_DISTRICT_002"],
                county_code_003=row["COUNTY_CODE_003"],
                place_code_004=row["PLACE_CODE_004"],
                critical_facility_006b=row["CRITICAL_FACILITY_006B"],
                facility_carried_007=row["FACILITY_CARRIED_007"],
                min_vert_clr_010=float(row["MIN_VERT_CLR_010"]) if row["MIN_VERT_CLR_010"] else None,
                kilometerpoint_011=float(row["KILOPOINT_011"]) if row["KILOPOINT_011"] else None,
                base_hwy_network_012=row["BASE_HWY_NETWORK_012"],
                lrs_inv_route_013a=row["LRS_INV_ROUTE_013A"],
                subroute_no_013b=row["SUBROUTE_NO_013B"],
                detour_kilos_019=int(row["DETOUR_KILOS_019"]) if row["DETOUR_KILOS_019"].isdigit() else None,
                toll_020=row["TOLL_020"],
                year_adt_030=int(row["YEAR_ADT_030"]) if row["YEAR_ADT_030"].isdigit() else None,
                appr_width_mt_032=float(row["APPR_WIDTH_MT_032"]) if row["APPR_WIDTH_MT_032"] else None,
                median_code_033=row["MEDIAN_CODE_033"],
                degrees_skew_034=int(row["DEGREES_SKEW_034"]) if row["DEGREES_SKEW_034"].isdigit() else None,
                structure_flared_035=row["STRUCTURE_FLARED_035"],
                railings_036a=row["RAILINGS_036A"],
                transitions_036b=row["TRANSITIONS_036B"],
                appr_rail_036c=row["APPR_RAIL_036C"],
                appr_rail_end_036d=row["APPR_RAIL_END_036D"],
                history_037=row["HISTORY_037"],
                navigation_038=row["NAVIGATION_038"],
                nav_vert_clr_mt_039=float(row["NAV_VERT_CLR_MT_039"]) if row["NAV_VERT_CLR_MT_039"] else None,
                nav_horr_clr_mt_040=float(row["NAV_HORR_CLR_MT_040"]) if row["NAV_HORR_CLR_MT_040"] else None,
                open_closed_posted_041=row["OPEN_CLOSED_POSTED_041"],
                service_on_042a=row["SERVICE_ON_042A"],
                service_und_042b=row["SERVICE_UND_042B"],
                operating_rating_064=float(row["OPERATING_RATING_064"]) if row["OPERATING_RATING_064"] else None,
                opr_rating_meth_063=row["OPR_RATING_METH_063"],
                inventory_rating_066=float(row["INVENTORY_RATING_066"]) if row["INVENTORY_RATING_066"] else None,
                inv_rating_meth_065=row["INV_RATING_METH_065"],
                structural_eval_067=row["STRUCTURAL_EVAL_067"],
                deck_geometry_eval_068=row["DECK_GEOMETRY_EVAL_068"],
                undclrenc_eval_069=row["UNDCLRENCE_EVAL_069"],
                posting_eval_070=row["POSTING_EVAL_070"],
                waterway_eval_071=row["WATERWAY_EVAL_071"],
                appr_road_eval_072=row["APPR_ROAD_EVAL_072"],
                work_proposed_075a=row["WORK_PROPOSED_075A"],
                work_done_by_075b=row["WORK_DONE_BY_075B"],
                imp_len_mt_076=float(row["IMP_LEN_MT_076"]) if row["IMP_LEN_MT_076"] else None,
                date_of_inspect_090=row["DATE_OF_INSPECT_090"],
                inspect_freq_months_091=row["INSPECT_FREQ_MONTHS_091"],
                fracture_092a=row["FRACTURE_092A"],
                undwater_look_see_092b=row["UNDWATER_LOOK_SEE_092B"],
                spec_inspect_092c=row["SPEC_INSPECT_092C"],
                fracture_last_date_093a=row["FRACTURE_LAST_DATE_093A"],
                undwater_last_date_093b=row["UNDWATER_LAST_DATE_093B"],
                spec_last_date_093c=row["SPEC_LAST_DATE_093C"],
                bridge_imp_cost_094=int(row["BRIDGE_IMP_COST_094"]) * 1000 if row["BRIDGE_IMP_COST_094"].isdigit() else None,
                roadway_imp_cost_095=int(row["ROADWAY_IMP_COST_095"]) * 1000 if row["ROADWAY_IMP_COST_095"].isdigit() else None,
                total_imp_cost_096=int(row["TOTAL_IMP_COST_096"]) * 1000 if row["TOTAL_IMP_COST_096"].isdigit() else None,
                year_of_imp_097=int(row["YEAR_OF_IMP_097"]) if row["YEAR_OF_IMP_097"].isdigit() else None,
                other_state_code_098a=row["OTHER_STATE_CODE_098A"],
                other_state_pcnt_098b=row["OTHER_STATE_PCNT_098B"],
                othr_state_struc_no_099=row["OTHR_STATE_STRUC_NO_099"],
                parallel_structure_101=row["PARALLEL_STRUCTURE_101"],
                temp_structure_103=row["TEMP_STRUCTURE_103"],
                deck_structure_type_107=row["DECK_STRUCTURE_TYPE_107"],
                surface_type_108a=row["SURFACE_TYPE_108A"],
                membrane_type_108b=row["MEMBRANE_TYPE_108B"],
                deck_protection_108c=row["DECK_PROTECTION_108C"],
                percent_adt_truck_109=int(row["PERCENT_ADT_TRUCK_109"]) if row["PERCENT_ADT_TRUCK_109"].isdigit() else None,
                national_network_110=row["NATIONAL_NETWORK_110"],
                pier_protection_111=row["PIER_PROTECTION_111"],
                bridge_len_ind_112=row["BRIDGE_LEN_IND_112"],
                scour_critical_113=row["SCOUR_CRITICAL_113"],
                future_adt_114=int(row["FUTURE_ADT_114"]) if row["FUTURE_ADT_114"].isdigit() else None,
                year_of_future_adt_115=int(row["YEAR_OF_FUTURE_ADT_115"]) if row["YEAR_OF_FUTURE_ADT_115"].isdigit() else None,
                min_nav_clr_mt_116=float(row["MIN_NAV_CLR_MT_116"]) if row["MIN_NAV_CLR_MT_116"] else None,
                fed_agency=row["FED_AGENCY"],
                submitted_by=row["SUBMITTED_BY"],
                strahnet_highway_100=row["STRAHNET_HIGHWAY_100"],
                traffic_direction_102=row["TRAFFIC_DIRECTION_102"],
                highway_system_104=row["HIGHWAY_SYSTEM_104"],
                federal_lands_105=row["FEDERAL_LANDS_105"],
            )

            bridge_core_objs.append(core)
            bridge_details_objs.append(details)

        except Exception as e:
            print(f"Skipping row due to error: {e}")
            continue

    db.bulk_save_objects(bridge_core_objs)
    db.bulk_save_objects(bridge_details_objs)
    db.commit()
    db.close()
    print(f"✅ Loaded {len(bridge_core_objs)} bridge records.")


if __name__ == "__main__":
    load_bridges_from_txt("app/db/data/PA22.txt")
    # load_bridges_from_txt("app/db/data/sample_bridges.txt")