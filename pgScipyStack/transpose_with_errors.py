import pandas as pd

for name in ["Fe"]:

    df_values = pd.read_csv(f"./data2/{name}-hodnoty.txt", delim_whitespace=True,
                            decimal=",", header=None, index_col=0, na_values="-")
    df_temp = pd.read_csv(f"./data2/{name}-chyba.txt", delim_whitespace=True,
                          decimal=",", header=None, index_col=0, na_values="-")
    df_errs = df_values * df_temp / 100

    T_df_values = df_values.T
    T_df_errs = df_errs.T

    final = pd.DataFrame()
    for col in T_df_values.columns:

        final[col] = T_df_values[col]
        final[f"{col}_err"] = T_df_errs[col]

    final.to_csv(f"./res2/{name}.csv", index=False)
