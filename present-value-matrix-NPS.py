
import numpy as np
import pandas as pd
import numpy_financial as npf


investment_values = [
    -91555, -99879, -108171, -115857, -139924, -152736, -166055, -180111,
    -194937, -223950, -241296, -259264, -278141, -389919, -419382, -457382,
    -502785, -545149, -589870, -636654, -685555, -737071, -790853, -847433,
    -911476, -1021366, -1110731, -1204689, -1265175, -1325662, -1520640,
    -1586995, -1653351, -1719705
]

discount_rate = 0.09
investment_cashflows = dict(zip(range(2022, 2056), investment_values))

# Function to calculate NPV using numpy_financial.npv
def calculate_full_npv_numpy(pensioner_death, spouse_death):
    last_survivor_death = max(pensioner_death, spouse_death)
    
    # Construct cash flow array from 2022 to last relevant year
    cashflows = [investment_cashflows.get(year, 0) for year in range(2022, last_survivor_death + 2)]

    # Add pension and lump sum payments
    cashflows[2056 - 2022] += 101264158  # Lumpsum in 2056
    for year in range(2056, last_survivor_death + 1):
        cashflows[year - 2022] += 4523132  # Annual pension
    cashflows[last_survivor_death + 1 - 2022] = 67509439  # Final lumpsum
    # Compute NPV using numpy_financial.npv
    return int(npf.npv(discount_rate, cashflows))  # Convert to int for output

def calculate_full_irr_numpy(pensioner_death, spouse_death):
    last_survivor_death = max(pensioner_death, spouse_death)
    
    # Construct cash flow array from 2022 to last relevant year
    cashflows = [investment_cashflows.get(year, 0) for year in range(2022, last_survivor_death + 2)]

    # Add pension and lump sum payments
    cashflows[2056 - 2022] += 101264158  # Lumpsum in 2056
    for year in range(2056, last_survivor_death + 1):
        cashflows[year - 2022] += 4523132  # Annual pension
    cashflows[last_survivor_death + 1 - 2022] = 67509439  # Final lumpsum

    # Compute IRR using numpy's np.irr
    irr = npf.irr(cashflows)
    return round(irr * 100, 2) if irr is not None else 0

# Redefining the years variable
years = np.arange(2056, 2076)  # Possible death years (2056-2075)

# Compute NPV matrix discounted to 2022
npv_matrix_2022 = pd.DataFrame(index=years, columns=years)
irr_matrix_2022 = pd.DataFrame(index=years, columns=years)

for p_death in years:
    for s_death in years:
        npv_matrix_2022.loc[p_death, s_death] = calculate_full_npv_numpy(p_death, s_death)
        irr_matrix_2022.loc[p_death, s_death] = calculate_full_irr_numpy(p_death, s_death)
    

# Save to CSV
npv_csv_filename_2022 = "nps_npv_matrix.csv"
irr_csv_filename_2022 = "nps_irr_matrix.csv"
npv_matrix_2022.to_csv(npv_csv_filename_2022)
irr_matrix_2022.to_csv(irr_csv_filename_2022,float_format="%.6f")

