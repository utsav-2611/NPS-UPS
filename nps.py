import numpy as np
import numpy_financial as npf
import pandas as pd

# Given investment values from 2022 to 2055
investment_values = [
    -91555, -99879, -108171, -115857, -139924, -152736, -166055, -180111,
    -194937, -223950, -241296, -259264, -278141, -389919, -419382, -457382,
    -502785, -545149, -589870, -636654, -685555, -737071, -790853, -847433,
    -911476, -1021366, -1110731, -1204689, -1265175, -1325662, -1520640,
    -1586995, -1653351, -1719705
]

# Constants
corpus_amount = 168773597  # Total corpus in NPS-1
pension_rate = 0.067  # 6.7% pension per year
discount_rate = 0  # 7.5% discount rate
pension_amount = pension_rate * corpus_amount  # Annual pension amount

death_years = list(range(2056, 2076))  # Death years from 2056 to 2075

# UPS-1 specific values
ups1_pensions = [
    8980070, 9510912, 10041753.6, 10572595.2, 11103436.8, 11634278.4,
    12165120, 12695961.6, 13226803.2, 13757644.8, 14368112.64, 15217459.2,
    16066805.76, 16916152.32, 17765498.88, 18614845.44, 19464192,
    20313538.56, 21162885.12, 22012231.68
]
ups1_lumpsum = 38186571  # Lump sum payment in 2056

# UPS-2 specific values
ups2_corpus = 115047514  # Total corpus for UPS-2
ups2_lumpsum = ups1_lumpsum + (0.60 * ups2_corpus)
ups2_pensions = [p * 0.40 for p in ups1_pensions]

# Store results
results = {"Death Year": death_years, "NPS-1 IRR": [], "NPS-1 NPV": [], "NPS-2 IRR": [], "NPS-2 NPV": [], "UPS-1 IRR": [], "UPS-1 NPV": [], "UPS-2 IRR": [], "UPS-2 NPV": []}

# Compute IRR and NPV for NPS-1
for death_year in death_years:
    cash_flows = investment_values[:]
    years_of_pension = death_year - 2056 + 1
    cash_flows.extend([pension_amount] * years_of_pension)
    cash_flows.append(corpus_amount)
    results["NPS-1 IRR"].append(npf.irr(cash_flows))
    results["NPS-1 NPV"].append(npf.npv(discount_rate, cash_flows))

# Compute IRR and NPV for NPS-2
for death_year in death_years:
    cash_flows = investment_values[:]
    corpus_remaining = corpus_amount * 0.40
    pension_amount_nps2 = pension_rate * corpus_remaining
    cash_flows.append(corpus_amount * 0.60 + pension_amount_nps2)
    years_of_pension = death_year - 2056
    cash_flows.extend([pension_amount_nps2] * years_of_pension)
    cash_flows.append(corpus_remaining)
    results["NPS-2 IRR"].append(npf.irr(cash_flows))
    results["NPS-2 NPV"].append(npf.npv(discount_rate, cash_flows))

# Compute IRR and NPV for UPS-1
for death_year in death_years:
    cash_flows = investment_values[:]
    cash_flows.append(ups1_lumpsum + ups1_pensions[0])
    years_of_pension = death_year - 2056
    cash_flows.extend(ups1_pensions[1:years_of_pension + 1])
    results["UPS-1 IRR"].append(npf.irr(cash_flows))
    results["UPS-1 NPV"].append(npf.npv(discount_rate, cash_flows))

# Compute IRR and NPV for UPS-2
for death_year in death_years:
    cash_flows = investment_values[:]
    cash_flows.append(ups2_lumpsum + ups2_pensions[0])
    years_of_pension = death_year - 2056
    cash_flows.extend(ups2_pensions[1:years_of_pension + 1])
    results["UPS-2 IRR"].append(npf.irr(cash_flows))
    results["UPS-2 NPV"].append(npf.npv(discount_rate, cash_flows))

# Convert results to DataFrame
df_results = pd.DataFrame(results)

# Save to CSV file
df_results.to_csv("nps_ups_irr_npv.csv", index=False)

print("Results saved to nps_ups_irr_npv.csv")
