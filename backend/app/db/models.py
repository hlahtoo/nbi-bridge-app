"""
SQLAlchemy models for bridge core, details, and metadata tables.
"""
from app.db.session import Base 
from sqlalchemy import Column, String, Integer, Float, CHAR, Date, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

# ───────────────────────────────────────────────
# Bridge Metadata Table
# ───────────────────────────────────────────────
class BridgeFieldMetadata(Base):
    __tablename__ = "bridge_field_metadata"

    table_name = Column(String(30), primary_key=True)
    field_name = Column(String(50), primary_key=True)
    data_type = Column(String(30))
    description = Column(String(255))

# ───────────────────────────────────────────────
# Core Bridge Info Table
# ───────────────────────────────────────────────
class BridgeCore(Base):
    __tablename__ = "bridge_core"
    
    # Identification
    structure_number_008 = Column(String(15), primary_key=True)

    # Location Info
    state_code_001 = Column(CHAR(3))
    lat_016 = Column(Float)
    long_017 = Column(Float)
    geom = Column(Geometry(geometry_type='POINT', srid=4326))
    location_009 = Column(String(50))

    # Classification & Route Info
    record_type_005a = Column(CHAR(1))
    route_prefix_005b = Column(CHAR(1))
    service_level_005c = Column(CHAR(1))
    maintenance_021 = Column(CHAR(2))
    owner_022 = Column(CHAR(2))
    functional_class_026 = Column(CHAR(2))

    # Structure & Traffic Info
    year_built_027 = Column(Integer)
    traffic_lanes_on_028a = Column(Integer)
    traffic_lanes_und_028b = Column(Integer)
    adt_029 = Column(Integer)
    design_load_031 = Column(CHAR(1))

    # Structure Types
    structure_kind_043a = Column(CHAR(1))
    structure_type_043b = Column(CHAR(2))

    # Condition Ratings
    deck_cond_058 = Column(CHAR(1))
    superstructure_cond_059 = Column(CHAR(1))
    substructure_cond_060 = Column(CHAR(1))
    channel_cond_061 = Column(CHAR(1))
    culvert_cond_062 = Column(CHAR(1))

    # Maintenance & Evaluation
    year_reconstructed_106 = Column(Integer)
    bridge_condition = Column(CHAR(1))
    lowest_rating = Column(Integer)
    deck_area = Column(Float)


# ───────────────────────────────────────────────
# Detailed Bridge Info Table
# ───────────────────────────────────────────────
class BridgeDetails(Base):
    __tablename__ = "bridge_details"
    
    # Identification 
    structure_number_008 = Column(String(15), ForeignKey("bridge_core.structure_number_008"), primary_key=True)

    # Descriptions & Features
    features_desc_006a = Column(String(50))
    critical_facility_006b = Column(CHAR(1))
    facility_carried_007 = Column(String(50))

    # Geometry & Location Details
    min_vert_clr_010 = Column(Float)
    kilometerpoint_011 = Column(Float)
    base_hwy_network_012 = Column(CHAR(1))
    lrs_inv_route_013a = Column(String(10))
    subroute_no_013b = Column(CHAR(1))
    route_number_005d = Column(CHAR(5))
    direction_005e = Column(CHAR(1))
    highway_district_002 = Column(CHAR(2))
    county_code_003 = Column(CHAR(3))
    place_code_004 = Column(CHAR(5))

    # Travel & Toll
    detour_kilos_019 = Column(Integer)
    toll_020 = Column(CHAR(1))

    # Traffic & Width
    year_adt_030 = Column(Integer)
    appr_width_mt_032 = Column(Float)
    median_code_033 = Column(CHAR(1))
    degrees_skew_034 = Column(Integer)

    # Structural Features
    structure_flared_035 = Column(CHAR(1))
    railings_036a = Column(CHAR(1))
    transitions_036b = Column(CHAR(1))
    appr_rail_036c = Column(CHAR(1))
    appr_rail_end_036d = Column(CHAR(1))

    # Navigation
    history_037 = Column(CHAR(1))
    navigation_038 = Column(CHAR(1))
    nav_vert_clr_mt_039 = Column(Float)
    nav_horr_clr_mt_040 = Column(Float)

    # Posting & Service
    open_closed_posted_041 = Column(CHAR(1))
    service_on_042a = Column(CHAR(1))
    service_und_042b = Column(CHAR(1))

    # Ratings
    operating_rating_064 = Column(Float)
    opr_rating_meth_063 = Column(CHAR(1))
    inventory_rating_066 = Column(Float)
    inv_rating_meth_065 = Column(CHAR(1))

    # Evaluations
    structural_eval_067 = Column(CHAR(1))
    deck_geometry_eval_068 = Column(CHAR(1))
    undclrenc_eval_069 = Column(CHAR(1))
    posting_eval_070 = Column(CHAR(1))
    waterway_eval_071 = Column(CHAR(1))
    appr_road_eval_072 = Column(CHAR(1))

    # Work Info
    work_proposed_075a = Column(CHAR(2))
    work_done_by_075b = Column(CHAR(1))
    imp_len_mt_076 = Column(Float)

    # Inspection Info
    date_of_inspect_090 = Column(String(5))  
    inspect_freq_months_091 = Column(CHAR(2))
    fracture_092a = Column(CHAR(3))
    undwater_look_see_092b = Column(CHAR(3))
    spec_inspect_092c = Column(CHAR(3))
    fracture_last_date_093a = Column(String(5))
    undwater_last_date_093b = Column(String(5))
    spec_last_date_093c = Column(String(5))

    # Costs
    bridge_imp_cost_094 = Column(Integer)
    roadway_imp_cost_095 = Column(Integer)
    total_imp_cost_096 = Column(Integer)
    year_of_imp_097 = Column(Integer)

    # Other State & Parallel Structures
    other_state_code_098a = Column(CHAR(3))
    other_state_pcnt_098b = Column(CHAR(2))
    othr_state_struc_no_099 = Column(String(15))
    parallel_structure_101 = Column(CHAR(1))

    # Deck Details
    temp_structure_103 = Column(CHAR(1))
    deck_structure_type_107 = Column(CHAR(1))
    surface_type_108a = Column(CHAR(1))
    membrane_type_108b = Column(CHAR(1))
    deck_protection_108c = Column(CHAR(1))

    # Traffic & Protection
    percent_adt_truck_109 = Column(Integer)
    national_network_110 = Column(CHAR(1))
    pier_protection_111 = Column(CHAR(1))
    bridge_len_ind_112 = Column(CHAR(1))
    scour_critical_113 = Column(CHAR(1))

    # Future Projections
    future_adt_114 = Column(Integer)
    year_of_future_adt_115 = Column(Integer)
    min_nav_clr_mt_116 = Column(Float)

    # System & Agency
    strahnet_highway_100 = Column(CHAR(1))
    traffic_direction_102 = Column(CHAR(1))
    highway_system_104 = Column(CHAR(1))
    federal_lands_105 = Column(CHAR(1))
    fed_agency = Column(CHAR(1))
    submitted_by = Column(CHAR(2))