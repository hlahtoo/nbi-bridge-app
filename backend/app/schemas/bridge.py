"""
Pydantic schema definitions for bridge core, detailed responses, and tile batch request.
"""
from pydantic import BaseModel
from typing import Optional, List

# Schema for summarized bridge core information
class BridgeCoreResponse(BaseModel):
    # Identification
    structure_number_008: str
    state_code_001: Optional[str]

    # Location
    lat_016: Optional[float]
    long_017: Optional[float]

    # Basic Construction Info
    year_built_027: Optional[int]
    year_reconstructed_106: Optional[int]

    # Traffic Info
    adt_029: Optional[int]  # Average Daily Traffic

    # Condition Ratings
    deck_cond_058: Optional[str]
    superstructure_cond_059: Optional[str]
    substructure_cond_060: Optional[str]
    channel_cond_061: Optional[str]
    culvert_cond_062: Optional[str]
    bridge_condition: Optional[str]
    lowest_rating: Optional[int]

    # Geometry
    deck_area: Optional[float]

    class Config:
        from_attributes = True


# Schema for full bridge detail data
class BridgeDetailsResponse(BaseModel):
    # Identification 
    structure_number_008: str

    # Descriptions & Features
    features_desc_006a: Optional[str]
    critical_facility_006b: Optional[str]
    facility_carried_007: Optional[str]

    # Geometry & Location Details
    min_vert_clr_010: Optional[float]
    kilometerpoint_011: Optional[float]
    base_hwy_network_012: Optional[str]
    lrs_inv_route_013a: Optional[str]
    subroute_no_013b: Optional[str]
    route_number_005d: Optional[str]
    direction_005e: Optional[str]
    highway_district_002: Optional[str]
    county_code_003: Optional[str]
    place_code_004: Optional[str]

    # Travel & Toll
    detour_kilos_019: Optional[int]
    toll_020: Optional[str]

    # Traffic & Width
    year_adt_030: Optional[int]
    appr_width_mt_032: Optional[float]
    median_code_033: Optional[str]
    degrees_skew_034: Optional[int]

    # Structural Features
    structure_flared_035: Optional[str]
    railings_036a: Optional[str]
    transitions_036b: Optional[str]
    appr_rail_036c: Optional[str]
    appr_rail_end_036d: Optional[str]

    # Navigation
    history_037: Optional[str]
    navigation_038: Optional[str]
    nav_vert_clr_mt_039: Optional[float]
    nav_horr_clr_mt_040: Optional[float]

    # Posting & Service
    open_closed_posted_041: Optional[str]
    service_on_042a: Optional[str]
    service_und_042b: Optional[str]

    # Ratings
    operating_rating_064: Optional[float]
    opr_rating_meth_063: Optional[str]
    inventory_rating_066: Optional[float]
    inv_rating_meth_065: Optional[str]

    # Evaluations
    structural_eval_067: Optional[str]
    deck_geometry_eval_068: Optional[str]
    undclrenc_eval_069: Optional[str]
    posting_eval_070: Optional[str]
    waterway_eval_071: Optional[str]
    appr_road_eval_072: Optional[str]

    # Work Info
    work_proposed_075a: Optional[str]
    work_done_by_075b: Optional[str]
    imp_len_mt_076: Optional[float]

    # Inspection Info
    date_of_inspect_090: Optional[str]
    inspect_freq_months_091: Optional[str]
    fracture_092a: Optional[str]
    undwater_look_see_092b: Optional[str]
    spec_inspect_092c: Optional[str]
    fracture_last_date_093a: Optional[str]
    undwater_last_date_093b: Optional[str]
    spec_last_date_093c: Optional[str]

    # Costs
    bridge_imp_cost_094: Optional[int]
    roadway_imp_cost_095: Optional[int]
    total_imp_cost_096: Optional[int]
    year_of_imp_097: Optional[int]

    # Other State & Parallel Structures
    other_state_code_098a: Optional[str]
    other_state_pcnt_098b: Optional[str]
    othr_state_struc_no_099: Optional[str]
    parallel_structure_101: Optional[str]

    # Deck Details
    temp_structure_103: Optional[str]
    deck_structure_type_107: Optional[str]
    surface_type_108a: Optional[str]
    membrane_type_108b: Optional[str]
    deck_protection_108c: Optional[str]

    # Traffic & Protection
    percent_adt_truck_109: Optional[int]
    national_network_110: Optional[str]
    pier_protection_111: Optional[str]
    bridge_len_ind_112: Optional[str]
    scour_critical_113: Optional[str]

    # Future Projection
    future_adt_114: Optional[int]
    year_of_future_adt_115: Optional[int]
    min_nav_clr_mt_116: Optional[float]

    # System & Agency
    strahnet_highway_100: Optional[str]
    traffic_direction_102: Optional[str]
    highway_system_104: Optional[str]
    federal_lands_105: Optional[str]
    fed_agency: Optional[str]
    submitted_by: Optional[str]

    class Config:
        from_attributes = True


# Schema for tile batch request payload
class TileBatchRequest(BaseModel):
    zoom: int
    tiles: List[List[int]]
