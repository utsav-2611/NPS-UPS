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

investment_cashflows = dict(zip(range(2022, 2056), investment_values))

discount_rate = 0.09

pension_payments_new = {
    2056: 3592028,
    2057: 3804364,
    2058: 4016701,
    2059: 4229038,
    2060: 4441374,
    2061: 4653711,
    2062: 4866048,
    2063: 5078384,
    2064: 5290721,
    2065: 5503057,
    2066: 5747244,
    2067: 6086983,
    2068: 6426722,
    2069: 6766460,
    2070: 7106199,
    2071: 7445938,
    2072: 7785676,
    2073: 8125415,
    2074: 8465154,
    2075: 8804892
}

# Lump sum in 2056
lumpsum_2056 = 107215079



# Function to calculate NPV for the new scenario
def calculate_npv_new(pensioner_death, spouse_death):
    last_survivor_death = max(pensioner_death, spouse_death)
    cashflows = [investment_cashflows.get(year, 0) for year in range(2022, last_survivor_death + 1)]

    # Add lump sum in 2056
    cashflows[2056 - 2022] += lumpsum_2056

    # Add pension payments
    for year in range(2056, last_survivor_death + 1):
        if year <= pensioner_death:
            cashflows[year - 2022] += pension_payments_new.get(year, 0)
        elif year <= spouse_death:
            cashflows[year - 2022] += int(0.6 * pension_payments_new.get(year, 0))  # 60% for spouse

    # Compute NPV
    return int(npf.npv(discount_rate, cashflows))

# Function to calculate IRR for the new scenario
def calculate_irr_new(pensioner_death, spouse_death):
    last_survivor_death = max(pensioner_death, spouse_death)
    cashflows = [investment_cashflows.get(year, 0) for year in range(2022, last_survivor_death + 1)]

    # Add lump sum in 2056
    cashflows[2056 - 2022] += lumpsum_2056

    # Add pension payments
    for year in range(2056, last_survivor_death + 1):
        if year <= pensioner_death:
            cashflows[year - 2022] += pension_payments_new.get(year, 0)
        elif year <= spouse_death:
            cashflows[year - 2022] += int(0.6 * pension_payments_new.get(year, 0))  # 60% for spouse


    # Compute IRR
    irr = npf.irr(cashflows)
    return round(irr*100, 2) if irr is not None else 0

# Redefining the years variable
years = np.arange(2056, 2076)  # Possible death years (2056-2075)

# Compute NPV and IRR matrices
npv_matrix_new = pd.DataFrame(index=years, columns=years)
irr_matrix_new = pd.DataFrame(index=years, columns=years)

for p_death in years:
    for s_death in years:
        npv_matrix_new.loc[p_death, s_death] = calculate_npv_new(p_death, s_death)
        irr_matrix_new.loc[p_death, s_death] = calculate_irr_new(p_death, s_death)

# Save to CSV files
csv_npv_new = "ups_npv_matrix.csv"
csv_irr_new = "ups_irr_matrix.csv"

npv_matrix_new.to_csv(csv_npv_new)
irr_matrix_new.to_csv(csv_irr_new, float_format="%.2f")


