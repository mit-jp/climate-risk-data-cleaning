import fix_differences as diff
import estimate_cdc_data as est
import organize_cdc_data as org
#pd.set_option('display.max_columns', None)

df = org.organize(r'CDC Wonder Data/Circulatory mortality at county level 2016.txt', r'CDC Wonder Data/Circulatory mortality at state level 2016.txt', r'CDC Wonder Data/Circulatory mortality at national level 2016.txt')
df_county, df_state, df_national = df[0], df[1], df[2]

df_county = diff.fix(df_county, 1, 1, 1) # fill in missing counties
df_county_no_estimates = df_county.round(5) # round data
df_county_no_estimates.to_csv(r'Parsed data/Circulatory Mortality.csv', index = False) #export without estimates

# Replace suppressed and unreliable values with estimates
df_county = est.estimate(df_national, df_state, df_county)

# Round
df_county = df_county.round(5)
df_state = df_state.round(5)
df_national = df_national.round(5)

# Export
df_county.to_csv(r'Parsed data/Circulatory Mortality with estimates.csv', index = False)
