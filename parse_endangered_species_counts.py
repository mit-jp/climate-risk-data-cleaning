import pandas as pd
import fix_differences as diff
import useful_analysis_functions as fns
# pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
df = pd.read_csv(r'Project data/endangered species data.csv')
df = df.drop(['GNAME', 'USESA_CD', 'USESA_STATE_STATUS', 'S_RANK', 'S_RANK_ROUNDED', 'INTERPRETED_USESA', 'ROUNDED_G_RANK', 'MAX_OBS_YEAR', 'COUNTY_NAME', 'STATE_CD', 'NSX_LINK', 'OCC_SRC'], axis=1)

df_numspec = df.groupby(['FIPS_CD']).count()
df_numspec = df_numspec.drop(['MAJOR_SUBGROUP1', 'G_COMNAME', 'G_RANK', 'BEST_EO_RANK'], axis=1)
df_numgrp = df.groupby(['FIPS_CD', 'MAJOR_SUBGROUP1']).count()
df_numgrp.reset_index(inplace=True)
df_numgrp = df_numgrp.pivot(index="FIPS_CD", columns="MAJOR_SUBGROUP1", values="ELEMENT_GLOBAL_ID")
df_numgrank = df.groupby(['FIPS_CD', 'G_RANK']).count()
df_numgrank.reset_index(inplace=True)
df_numgrank = df_numgrank.pivot(index="FIPS_CD", columns="G_RANK", values="ELEMENT_GLOBAL_ID")
df_numeorank = df.groupby(['FIPS_CD', 'BEST_EO_RANK']).count()
df_numeorank.reset_index(inplace=True)
df_numeorank = df_numeorank.pivot(index="FIPS_CD", columns="BEST_EO_RANK", values="ELEMENT_GLOBAL_ID")
df = pd.concat([df_numspec, df_numgrp, df_numgrank, df_numeorank], axis=1)
df = df.reset_index(col_level=1)
df = fns.split_state_and_county_codes(df, 'FIPS_CD')
df = pd.concat([df.iloc[:, 329:331], df.iloc[:, 1:329]], axis=1)
df = diff.fix(df, 1, 1, 1) # fill in missing counties
df.to_csv(r'Parsed data/Endangered species counts.csv', index = False)