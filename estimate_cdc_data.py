import cdc_estimation_functions as rg

def estimate(df_national, df_state, df_county):
    # Calculate the average death rate for suppressed counties
    df_state, df_county = rg.death_rate_suppressed_counties(df_state, df_county)

    # Replace suppressed values with calculated averages
    df_county = rg.replace_suppressed_values(df_national, df_state, df_county)

    # Create a hashmap to represent the regional groupings
    regional_groupings = rg.create_regional_hashmap()

    # Create the subtables to be used in different scenarios for calculating unreliable values
    df_county_sub_20_regional0_5, df_county_sub_20_regional5_25, df_county_sub_20_regional25, df_county_sub_20_state0_5, df_county_sub_20_state5_25, df_county_sub_20_state25 = rg.unreliable_subtables(
        df_state, df_county)

    # Replace values under 20 with calculated averages
    df_county = rg.replace_unreliable_values(df_county, df_county_sub_20_state0_5, df_county_sub_20_state5_25,
                                             df_county_sub_20_state25, df_county_sub_20_regional0_5,
                                             df_county_sub_20_regional5_25, df_county_sub_20_regional25,
                                             regional_groupings)
    return df_county