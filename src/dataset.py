import itertools

import numpy as np

GLOBAL_REPRODUCIBILITY_SEED = 1

DATA_DIR = 'C:/Users/kaius/Documents/Kai/Praktika, Freiwilligenarbeit und Führerschein/ECB'
# DATA_DIR = '/p/projects/eubucco/data/2-database-city-level-v0_1'
METADATA_DIR = '/p/projects/eubucco/data/3-ml-inputs'
# DATA_DIR = os.path.realpath(os.path.join(__file__, '..', '..', 'data', 'geometry'))
# METADATA_DIR = os.path.realpath(os.path.join(__file__, '..', '..', 'metadata'))

# age bands ~ according to English Housing Survey (EHS) as done in https://doi.org/10.1016/j.compenvurbsys.2018.08.004
EHS_AGE_BINS = [0, 1915, 1945, 1965, 1980, 2000, np.inf]
TABULA_AGE_BINS = {
    'harmonized': [0, 1900, 1945, 1960, 1970, 1980, 1990, 2000, 2010, np.inf], # by Flo
    # 'harmonized': [0, 1900, 1945, 1970, 1980, 1990, 2000, 2010, np.inf], # by Peter
    'netherlands': [0, 1965, 1975, 1992, 2006, 2015, 2051],
    'france': [0, 1915, 1949, 1968, 1975, 1982, 1990, 2000, 2006, 2013, 2051],
    'netherlands_small': [0, 1915, 1945, 1965, 1975, 1983, 1992, 1999, 2006, 2015, 2051],
    'france_small': [0, 1915, 1949, 1959, 1968, 1975, 1982, 1990, 1995, 2000, 2006, 2013, 2051],
}

RESIDENTIAL_TYPE = 'residential'
BUILDING_TYPES = [
    'Résidentiel',
    'Annexe',
    'Agricole',
    'Commercial et services',
    'Industriel',
    'Religieux',
    'Sportif',
    # Indifférencié == n.a.
]

#AGE_ATTRIBUTE = 'age'
AGE_ATTRIBUTE = 'YearBlt_new2'
TYPE_ATTRIBUTE = 'type'
HEIGHT_ATTRIBUTE = 'height'
AUX_VARS = [
    'id',
    'id_source',
    'source_file',
    'city',
    'TouchesIndexes',
    'type',
    'type_source',
    'age_wsf',
    'block',
    'block_bld_ids',
    'sbb',
    'sbb_bld_ids',
    'geometry',
    'country',
]
BUILDING_FEATURES = [
    'FootprintArea',
    'Perimeter',
    'Phi',
    'LongestAxisLength',
    'Elongation',
    'Convexity',
    'Orientation',
    'Corners',
    'CountTouches',
    'SharedWallLength',
    'lat',
    'lon',
]
BUILDING_FEATURES_NEIGHBORHOOD = [
    'av_convexity_within_buffer_100',
    'av_convexity_within_buffer_500',
    'av_elongation_within_buffer_100',
    'av_elongation_within_buffer_500',
    'av_footprint_area_within_buffer_100',
    'av_footprint_area_within_buffer_500',
    'av_orientation_within_buffer_100',
    'av_orientation_within_buffer_500',
    'buildings_within_buffer_100',
    'buildings_within_buffer_500',
    'std_convexity_within_buffer_100',
    'std_convexity_within_buffer_500',
    'std_elongation_within_buffer_100',
    'std_elongation_within_buffer_500',
    'std_footprint_area_within_buffer_100',
    'std_footprint_area_within_buffer_500',
    'std_orientation_within_buffer_100',
    'std_orientation_within_buffer_500',
    'total_ft_area_within_buffer_100',
    'total_ft_area_within_buffer_500',
]
BLOCK_FEATURES = [
    'AvBlockFootprintArea',
    'BlockConvexity',
    'BlockCorners',
    'BlockElongation',
    'BlockLength',
    'BlockLongestAxisLength',
    'BlockOrientation',
    'BlockPerimeter',
    'BlockTotalFootprintArea',
    'StdBlockFootprintArea',
]
BLOCK_FEATURES_NEIGHBORHOOD = [
    'blocks_within_buffer_100',
    'blocks_within_buffer_500',
    'av_block_av_footprint_area_within_buffer_100',
    'av_block_av_footprint_area_within_buffer_500',
    'av_block_footprint_area_within_buffer_100',
    'av_block_footprint_area_within_buffer_500',
    'av_block_length_within_buffer_100',
    'av_block_length_within_buffer_500',
    'av_block_orientation_within_buffer_100',
    'av_block_orientation_within_buffer_500',
    'std_block_av_footprint_area_within_buffer_100',
    'std_block_av_footprint_area_within_buffer_500',
    'std_block_footprint_area_within_buffer_100',
    'std_block_footprint_area_within_buffer_500',
    'std_block_length_within_buffer_100',
    'std_block_length_within_buffer_500',
    'std_block_orientation_within_buffer_100',
    'std_block_orientation_within_buffer_500',
]
SBB_FEATURES = [
    'street_based_block_area',
    'street_based_block_corners',
    'street_based_block_phi',
]
STREET_ONLY_FEATURES = [
    'dist_to_closest_int',
    'distance_to_closest_street',
    'street_length_closest_street',
    'street_openness_closest_street',
    'street_width_av_closest_street',
    'street_width_std_closest_street',
]

STREET_FEATURES = [
    'street_based_block_area',
    'street_based_block_corners',
    'street_based_block_phi',

    'dist_to_closest_int',
    'distance_to_closest_street',
    'street_length_closest_street',
    'street_openness_closest_street',
    'street_width_av_closest_street',
    'street_width_std_closest_street',
]
SBB_FEATURES_NEIGHBORHOOD = [
    'street_based_block_av_area_inter_buffer_100',
    'street_based_block_av_area_inter_buffer_500',
    'street_based_block_av_phi_inter_buffer_100',
    'street_based_block_av_phi_inter_buffer_500',
    'street_based_block_number_inter_buffer_100',
    'street_based_block_number_inter_buffer_500',
    'street_based_block_std_area_inter_buffer_100',
    'street_based_block_std_area_inter_buffer_500',
    'street_based_block_std_orientation_inter_buffer_100',
    'street_based_block_std_orientation_inter_buffer_500',
    'street_based_block_std_phi_inter_buffer_100',
    'street_based_block_std_phi_inter_buffer_500',
]
STREET_ONLY_FEATURES_NEIGHBORHOOD = [
    'intersection_count_within_100',
    'intersection_count_within_500',
    'street_length_av_within_buffer_100',
    'street_length_av_within_buffer_500',
    'street_length_std_within_buffer_100',
    'street_length_std_within_buffer_500',
    'street_length_total_within_buffer_100',
    'street_length_total_within_buffer_500',
    'street_width_av_within_buffer_100',
    'street_width_av_within_buffer_500',
    'street_width_std_within_buffer_100',
    'street_width_std_within_buffer_500'
]
STREET_FEATURES_NEIGHBORHOOD = [
    'street_based_block_av_area_inter_buffer_100',
    'street_based_block_av_area_inter_buffer_500',
    'street_based_block_av_phi_inter_buffer_100',
    'street_based_block_av_phi_inter_buffer_500',
    'street_based_block_number_inter_buffer_100',
    'street_based_block_number_inter_buffer_500',
    'street_based_block_std_area_inter_buffer_100',
    'street_based_block_std_area_inter_buffer_500',
    'street_based_block_std_orientation_inter_buffer_100',
    'street_based_block_std_orientation_inter_buffer_500',
    'street_based_block_std_phi_inter_buffer_100',
    'street_based_block_std_phi_inter_buffer_500',

    'intersection_count_within_100',
    'intersection_count_within_500',
    'street_length_av_within_buffer_100',
    'street_length_av_within_buffer_500',
    'street_length_std_within_buffer_100',
    'street_length_std_within_buffer_500',
    'street_length_total_within_buffer_100',
    'street_length_total_within_buffer_500',
    'street_width_av_within_buffer_100',
    'street_width_av_within_buffer_500',
    'street_width_std_within_buffer_100',
    'street_width_std_within_buffer_500'
]
STREET_FEATURES_CENTRALITY = [
    'street_betweeness_global_av_within_buffer_100',
    'street_betweeness_global_av_within_buffer_500',
    'street_betweeness_global_max_within_buffer_100',
    'street_betweeness_global_max_within_buffer_500',
    'street_betweeness_global_closest_street',
    'street_closeness_global_closest_street',
    'street_closeness_500_closest_street',
    'street_closeness_500_av_within_buffer_100',
    'street_closeness_500_av_within_buffer_500',
    'street_closeness_500_max_within_buffer_100',
    'street_closeness_500_max_within_buffer_500',
]
CITY_FEATURES = [
    'total_buildings_city',
    'n_detached_buildings',
    'total_buildings_footprint_city',
    'av_building_footprint_city',
    'std_building_footprint_city',

    'blocks_2_to_4',
    'blocks_5_to_9',
    'blocks_10_to_19',
    'blocks_20_to_inf',

    'total_length_street_city',
    'av_length_street_city',
    'intersections_count',

    'av_area_block_city',
    'std_area_block_city',
    'total_number_block_city',
]
LANDUSE_FEATURES = [
    'bld_in_lu_agricultural',
    'bld_in_lu_industrial_commercial',
    'bld_in_lu_natural',
    'bld_in_lu_other',
    'bld_in_lu_roads',
    'bld_in_lu_urban_fabric',
    'bld_in_lu_urban_green',
    'bld_in_lu_water',
    'bld_in_lu_ocean_country',
    'bld_in_lu_railways',
    'bld_in_lu_ports_airports',
    'lu_ocean_country_within_buffer_100',
    'lu_natural_within_buffer_100',
    'lu_industrial_commercial_within_buffer_100',
    'lu_other_within_buffer_100',
    'lu_water_within_buffer_100',
    'lu_urban_green_within_buffer_100',
    'lu_agricultural_within_buffer_100',
    'lu_railways_within_buffer_100',
    'lu_urban_fabric_within_buffer_100',
    'lu_ports_airports_within_buffer_100',
    'lu_roads_within_buffer_100',
    'lu_ocean_country_within_buffer_500',
    'lu_natural_within_buffer_500',
    'lu_industrial_commercial_within_buffer_500',
    'lu_other_within_buffer_500',
    'lu_water_within_buffer_500',
    'lu_urban_green_within_buffer_500',
    'lu_agricultural_within_buffer_500',
    'lu_railways_within_buffer_500',
    'lu_urban_fabric_within_buffer_500',
    'lu_ports_airports_within_buffer_500',
    'lu_roads_within_buffer_500'
]
SELECTED_FEATURES = [
    'total_ft_area_within_buffer_100',
    'street_closeness_global_closest_street',
    'StdBlockFootprintArea',
    'street_width_av_closest_street',
    'std_convexity_within_buffer_100',
    'av_convexity_within_buffer_100',
    'lon',
    'Phi',
    'street_betweeness_global_closest_street',
    'Convexity',
    'BlockLongestAxisLength',
    'street_width_std_within_buffer_500',
    'street_width_std_closest_street',
    'std_block_av_footprint_area_within_buffer_100',
    'distance_to_closest_street',
    'total_ft_area_within_buffer_500',
    'AvBlockFootprintArea',
    'lat',
    'BlockElongation',
    'BlockTotalFootprintArea',
    'street_betweeness_global_av_within_buffer_100',
    'Corners',
    'FootprintArea',
    'std_block_footprint_area_within_buffer_100',
    'buildings_within_buffer_100',
    'buildings_within_buffer_500',
    'av_footprint_area_within_buffer_100',
    'av_elongation_within_buffer_100'
]
RCA_FEATURES = [
    'PropertyKey_ID',
    'Deal_id',
    'Property_id',
    'Portfolio',
    'Property_nb',
    'Status_tx',	
    'Status_dt',
    'IntConveyed_nb',
    'IntConvey_tx',
    'TransType_tx',
    'PartialInterestType_tx',
    'PropertyName'
    'Address_tx'
    'City_tx',
    'State_cd',
    'Zip_cd',
    'Country_tx',
    'Region',
    'RCA_Metros_tx',
    'RCA_Markets_tx',
    'CBD_fg',
    'Main Type',
    'SubType',
    'OutputCategory1',
    'OutputCategory2',
    'Tenancy_tx',
    'YearRenuExp_nb',
    'NumberBldgs_nb',
    'NumberFloors_nb',
    'Occupancy_rate',
    'Price',
    'StatusPriceAdjustedUSD_amt',
    'PriceEuro',
    'StatusPriceAdjustedEUR_amt',
    'PSF/PPU',
    'CapRate',
    'CapQualifyer',
    'DealQualifyer',
    'SqFt_nb',
    'NumberUnits_nb',
    'BuyerName1',
    'BuyerJV',
    'BuyerName2',
    'BuyerJV2',
    'BuyerName3',
    'SellerName1',
    'SellerJV',
    'SellerName2',
    'SellerJV2',
    'SellerName3',
    'Tenant1',
    'Tenant2',
    'Tenant3',
    'BuyerObjective',
    'Deal_Update_dt',
    'Property_Update_dt',
    'Prior_Sale_dt',
    'Prior_Sale_Price_at',
    'Excess_Land_Potential_fg',
    'Leaseback_fg',
    'LeasebackType_tx',
    'County_nm',
    'Land_Area_Acres_nb',
    'BuyerCapGroup1',
    'BuyerCapGroup2',
    'BuyerCapGroup3',
    'BuyerCapType1',
    'BuyerCapType2',
    'BuyerCapType3',
    'BuyerCountry',
    'BuyerCountry2',
    'BuyerCountry3',
    'SellerCapGroup1',
    'SellerCapGroup2',
    'SellerCapGroup3',
    'SellerCapType1',
    'SellerCapType2',
    'SellerCapType3',
    'SellerCountry',
    'SellerCountry2',
    'SellerCountry3',
    'SellerBrokerageGroup',
    'BuyerBrokerageGroup',
    'CBSA_cd',
    'Lat_nb',
    'Lon_nb',
    'FIPS_cd',
    'Metro_Div_cd',
    'HotelFranchise_nm',
    'Mtg_Space_nb',
    'DevMainType',
    'DevSubType1',
    'DevSubType2',
    'DevCalcSqFt',
    'DevComments',
    'ImprovedType_tx',
    'ImprovedComments_tx',
    'DevPriorUse_tx',
    'PricePerLandAcre',
    'PricePerLandSqFt',
    'PricePerBldSqFt',
    'PercentProjectCost',
    'DevFloors_nb',
    'DevComplete_dt',
    'Website_tx',
    'Lender',
    'Loan_amt',
    'Lender_Interest_Rate_nb',
    'Lender_Int_Rate_Type_tx',
    'Loan_Term_Mths_tx',
    'Loan_Maturity_dt',
    'Lender_Comments_tx',
    'Loan_Orig_dt',
    'Loan_Int_Method_tx',
    'Loan_Cross_Default_fg',
    'Loan_PI_Payment_amt',
    'Loan_Orig_IO_Terms_nb',
    'Loan_Int_Method_IO_tx',
    'Loan_Amort_Orig_nb',
    'DSCR_nb',
    'Loan_LTV_Orig_nb',
    'Loan_PrePay_tx',
    'Mort_Brokerage_name',
    'BuyerAssumedDebt',
    'Originator_tx',
    'CMBS_fg',
    'Deal5M_fg',
    'Deal10M_fg',
    'EligibleForVolume_fg',
    'EligibleForPPU_fg',
    'EligibleForCapRates_fg',
    'Active_fg',
    'ModificationType_tx',
    'MaxChanged_dt'
]

RCA_FEATURES_CAT = [
    'Portfolio',
    'Status_tx',
    'Status_dt',
    'IntConvey_tx',
    'TransType_tx',
    'PartialInterestType_tx',
    'PropertyName',
    'Address_tx',
    'City_tx',
    'State_cd',
    'Zip_cd',
    'Country_tx',
    'Region',
    'RCA_Metros_tx',
    'RCA_Markets_tx',
    'CBD_fg',
    'Main Type',
    'SubType',
    'OutputCategory1',
    'OutputCategory2',
    'Tenancy_tx',
    'NumberFloors_nb',
    'CapQualifyer',
    'DealQualifyer',
    'BuyerName1',
    'BuyerJV',
    'BuyerName2',
    'BuyerJV2',
    'BuyerName3',
    'SellerName1',
    'SellerJV',
    'SellerName2',
    'Tenant1',
    'Tenant2',
    'Tenant3',
    'BuyerObjective',
    'Deal_Update_dt',
    'Property_Update_dt',
    'Prior_Sale_dt',
    'LeasebackType_tx',
    'County_nm',
    'BuyerCapGroup1',
    'BuyerCapGroup2',
    'BuyerCapGroup3',
    'BuyerCapType1',
    'BuyerCapType2',
    'BuyerCapType3',
    'BuyerCountry',
    'BuyerCountry2',
    'BuyerCountry3',
    'SellerCapGroup1',
    'SellerCapGroup2',
    'SellerCapType1',
    'SellerCapType2',
    'SellerCountry',
    'SellerCountry2',
    'SellerBrokerageGroup',
    'BuyerBrokerageGroup',
    'HotelFranchise_nm',
    'DevMainType',
    'DevSubType1',
    'DevSubType2',
    'DevComments',
    'ImprovedType_tx',
    'ImprovedComments_tx',
    'DevPriorUse_tx',
    'DevComplete_dt',
    'Website_tx',
    'Lender',
    'Lender_Int_Rate_Type_tx',
    'Loan_Maturity_dt',
    'Lender_Comments_tx',
    'Loan_Orig_dt',
    'Loan_Cross_Default_fg',
    'Originator_tx',
    'MaxChanged_dt'
]

RCA_FEATURES_SUB = [
    "PropertyKey_ID",
    "Deal_id",
    "Property_id",
    "Status_tx",
    "Status_dt",
    "TransType_tx",
    "Country_tx",
    "Main Type",
    "SubType",
    "DealQualifyer",
    "Deal_Update_dt",
    "Property_Update_dt",
    "Excess_Land_Potential_fg",
    "Lat_nb",
    "Lon_nb",
    "BuyerAssumedDebt",
    "CMBS_fg",
    "Deal5M_fg",
    "Deal10M_fg",
    "EligibleForVolume_fg",
    "EligibleForPPU_fg",
    "EligibleForCapRates_fg",
    "Active_fg",
    "MaxChanged_dt",
    "year",
    "age_bracket",
    "Property_nb",
    "Price",
    "StatusPriceAdjustedUSD_amt",
    "PriceEuro",
    "StatusPriceAdjustedEUR_amt",
    "BuyerObjective",
    "BuyerCapGroup1",
    "BuyerCapType1",
    "PropertyName",
    "Region",
    "State_cd",
    "RCA_Metros_tx",
    "SellerCapGroup1",
    "SellerCapType1",
    "County_nm",
    "RCA_Markets_tx",
    "Leaseback_fg",
    "City_tx",
    "CBD_fg",
    "PSF/PPU",
    "Zip_cd",
    "BuyerCountry",
    "BuyerName1",
    "Address_tx",
    "SellerName1",
    "SellerCountry",
    "Tenancy_tx",
    "SqFt_nb",
    "NumberBldgs_nb",
    "NumberFloors_nb"
]

RCA_FEATURES_SUBCAT = [
    'Status_tx',
    'Status_dt',
    'TransType_tx',
    'Country_tx',
    'Main Type',
    'SubType',
    'DealQualifyer',
    'Deal_Update_dt',
    'Property_Update_dt',
    'MaxChanged_dt',
    'age_bracket',
    'BuyerObjective',
    'BuyerCapGroup1',
    'BuyerCapType1',
    'PropertyName',
    'Region',
    'State_cd',
    'RCA_Metros_tx',
    'SellerCapGroup1',
    'SellerCapType1',
    'County_nm',
    'RCA_Markets_tx',
    'Leaseback_fg',
    'City_tx',
    'CBD_fg',
    'Zip_cd',
    'BuyerCountry',
    'BuyerName1',
    'Address_tx',
    'SellerName1',
    'SellerCountry',
    'Tenancy_tx',
    'NumberFloors_nb'
]




#TARGET_ATTRIBUTES = [AGE_ATTRIBUTE, TYPE_ATTRIBUTE, HEIGHT_ATTRIBUTE, 'floors']
TARGET_ATTRIBUTES = [AGE_ATTRIBUTE]

BUILDING_FEATURES_ALL = BUILDING_FEATURES + BUILDING_FEATURES_NEIGHBORHOOD
BLOCK_FEATURES_ALL = BLOCK_FEATURES + BLOCK_FEATURES_NEIGHBORHOOD
STREET_FEATURES_ALL = STREET_FEATURES + STREET_FEATURES_NEIGHBORHOOD + STREET_FEATURES_CENTRALITY

NEIGHBORHOOD_FEATURES = BUILDING_FEATURES_NEIGHBORHOOD + BUILDING_FEATURES_NEIGHBORHOOD + STREET_FEATURES_NEIGHBORHOOD + STREET_FEATURES_CENTRALITY
SPATIALLY_EXPLICIT_FEATURES = BUILDING_FEATURES + BLOCK_FEATURES + STREET_FEATURES

# FEATURES = list(itertools.chain(
#     BUILDING_FEATURES,
#     BUILDING_FEATURES_NEIGHBORHOOD,
#     BLOCK_FEATURES,
#     BLOCK_FEATURES_NEIGHBORHOOD,
#     STREET_FEATURES,
#     STREET_FEATURES_NEIGHBORHOOD,
#     STREET_FEATURES_CENTRALITY,
#     CITY_FEATURES,
#     # LANDUSE_FEATURES,
# ))
FEATURES = list(itertools.chain(
    RCA_FEATURES_SUB
))