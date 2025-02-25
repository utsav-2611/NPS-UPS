import numpy as np
import matplotlib.pyplot as plt
import numpy_financial as npf


def calculate_irr(lump_sum_percentage, investment_years, investment_values, corpus, pension_values, start_pension_year, corpus_return_year):
    cash_flows = dict(zip(investment_years, investment_values))
    
    lump_sum = lump_sum_percentage * corpus + 38186571
    adjusted_pension_values = {year: pension_values[year] * (1 - lump_sum_percentage) for year in pension_values}
    
    # Add lump sum withdrawal and pension payout in 2056
    cash_flows[2056] = lump_sum + adjusted_pension_values[2056]
    
    # Add pension payouts from 2057 to 2075
    for year in range(start_pension_year + 1, corpus_return_year):
        cash_flows[year] = adjusted_pension_values[year]
    
    # Add final corpus return in 2076
    cash_flows[corpus_return_year] = 0
    
    # Sort cash flows in order
    sorted_years = sorted(cash_flows.keys())
    cash_flow_series = [cash_flows[year] for year in sorted_years]
    
    # Compute IRR
    irr = npf.irr(cash_flow_series)
    return irr

def calculate_npv(discount_rate, lump_sum_percentage, investment_years, investment_values, corpus, pension_values, start_pension_year, corpus_return_year):
    cash_flows = dict(zip(investment_years, investment_values))
    
    lump_sum = lump_sum_percentage * corpus + 38186571
    adjusted_pension_values = {year: pension_values[year] * (1 - lump_sum_percentage) for year in pension_values}
    
    # Add lump sum withdrawal and pension payout in 2056
    cash_flows[2056] = lump_sum + adjusted_pension_values[2056]
    
    # Add pension payouts from 2057 to 2075
    for year in range(start_pension_year + 1, corpus_return_year):
        cash_flows[year] = adjusted_pension_values[year]
    
    # Add final corpus return in 2076
    cash_flows[corpus_return_year] = 0
    
    # Sort cash flows in order
    sorted_years = sorted(cash_flows.keys())
    cash_flow_series = [cash_flows[year] for year in sorted_years]
    
    # Compute NPV
    npv = npf.npv(discount_rate, cash_flow_series)
    return npv

# Given investment data
years = list(range(2022, 2056))
investments = [-91555, -99879, -108171, -115857, -139924, -152736, -166055, -180111, -194937, -223950,
               -241296, -259264, -278141, -389919, -419382, -457382, -502785, -545149, -589870, -636654,
               -685555, -737071, -790853, -847433, -911476, -1021366, -1110731, -1204689, -1265175,
               -1325662, -1520640, -1586995, -1653351, -1719705]

# Parameters
corpus = 115047514
pension_values = {
    2056: 8980070, 2057: 9510912, 2058: 10041753.6, 2059: 10572595.2, 2060: 11103436.8,
    2061: 11634278.4, 2062: 12165120, 2063: 12695961.6, 2064: 13226803.2, 2065: 13757644.8,
    2066: 14368112.64, 2067: 15217459.2, 2068: 16066805.76, 2069: 16916152.32, 2070: 17765498.88,
    2071: 18614845.44, 2072: 19464192, 2073: 20313538.56, 2074: 21162885.12, 2075: 22012231.68, 2076: 0
}
start_pension_year = 2056
corpus_return_year = 2076
discount_rate = 0.08  # 7% discount rate

# Compute IRR for different withdrawal percentages
withdrawal_percentages = np.arange(0, 61, 1) / 100  # 0% to 60% in steps of 5%
irrs = [calculate_irr(wp, years, investments, corpus, pension_values, start_pension_year, corpus_return_year) for wp in withdrawal_percentages]

# Compute NPV for different withdrawal percentages
npvs = [calculate_npv(discount_rate, wp, years, investments, corpus, pension_values, start_pension_year, corpus_return_year) for wp in withdrawal_percentages]

# # Plot IRR results
# plt.figure(figsize=(10, 5))
# plt.plot(withdrawal_percentages * 100, np.array(irrs) * 100, marker='o', linestyle='-', label='IRR')
# plt.xlabel("Lump Sum Withdrawal (%)")
# plt.ylabel("IRR (%)")
# plt.title("Impact of Lump Sum Withdrawal on IRR (Fixed Pension)")
# plt.grid()
# plt.legend()
# plt.show()

# # Plot NPV results with y-axis in 10^7 scale
# plt.figure(figsize=(10, 5))
# plt.plot(withdrawal_percentages * 100, npvs, marker='s', linestyle='-', color='r', label='NPV')
# plt.xlabel("Lump Sum Withdrawal (%)")
# plt.ylabel("NPV (in ₹10^7)")
# # plt.ticklabel_format(style='sci', axis='y', scilimits=(7,7))  # Adjust scale
# plt.title("Impact of Lump Sum Withdrawal on NPV (Fixed Pension)")
# plt.grid()
# plt.legend()
# plt.show()


# Plot IRR results
plt.figure(figsize=(10, 5))
plt.plot(withdrawal_percentages * 100, np.array(irrs) * 100, linestyle='-', label='IRR')
plt.axhline(y=13.23, color='gray', linestyle='--', label='IRR = 13.23%')

# Find intersection point for IRR
diff = np.abs(np.array(irrs) * 100 - 13.23)
intersection_index = np.argmin(diff)
plt.scatter(withdrawal_percentages[intersection_index] * 100, irrs[intersection_index] * 100, color='red', label='Intersection')
plt.annotate(f"({withdrawal_percentages[intersection_index] * 100:.0f}%, {irrs[intersection_index] * 100:.2f}%)", 
             (withdrawal_percentages[intersection_index] * 100, irrs[intersection_index] * 100),
             textcoords="offset points", xytext=(-30,-10), ha='center')

plt.xlabel("Lump Sum Withdrawal (%)")
plt.ylabel("IRR (%)")
plt.title("Impact of Lump Sum Withdrawal on IRR")
plt.grid()
plt.legend()
plt.show()

# Plot NPV results
plt.figure(figsize=(10, 5))
plt.plot(withdrawal_percentages * 100, npvs, linestyle='-', color='r', label='NPV')
plt.axhline(y=7560000, color='gray', linestyle='--', label='NPV = 27,98,000')

# Find intersection point for NPV
diff_npv = np.abs(np.array(npvs) - 7560000)
intersection_index_npv = np.argmin(diff_npv)
plt.scatter(withdrawal_percentages[intersection_index_npv] * 100, npvs[intersection_index_npv], color='blue', label='Intersection')
plt.annotate(f"({withdrawal_percentages[intersection_index_npv] * 100:.0f}%, {npvs[intersection_index_npv]:,.0f})", 
             (withdrawal_percentages[intersection_index_npv] * 100, npvs[intersection_index_npv]),
             textcoords="offset points", xytext=(-30,-10), ha='center')

plt.xlabel("Lump Sum Withdrawal (%)")
plt.ylabel("NPV")
plt.title("Impact of Lump Sum Withdrawal on NPV")
plt.grid()
plt.legend()
plt.show()
