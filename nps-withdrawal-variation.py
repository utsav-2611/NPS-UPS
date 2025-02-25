import numpy as np
import matplotlib.pyplot as plt
import numpy_financial as npf


def calculate_irr(lump_sum_percentage, investment_years, investment_values, corpus, pension_rate, start_pension_year, end_pension_year, corpus_return_year):
    cash_flows = dict(zip(investment_years, investment_values))
    
    lump_sum = lump_sum_percentage * corpus
    annuity_corpus = corpus - lump_sum
    annual_pension = pension_rate * annuity_corpus
    
    # Add lump sum withdrawal in 2056
    cash_flows[2056] = lump_sum + annual_pension
    
    # Add pension payouts from 2056 to 2075
    for year in range(start_pension_year+1, end_pension_year + 1):
        cash_flows[year] = annual_pension
    
    # Add corpus return in 2076
    cash_flows[corpus_return_year] = annuity_corpus
    
    # Sort cash flows in order
    sorted_years = sorted(cash_flows.keys())
    cash_flow_series = [cash_flows[year] for year in sorted_years]
    
    # Compute IRR
    irr = npf.irr(cash_flow_series)
    return irr

def calculate_npv(discount_rate, lump_sum_percentage, investment_years, investment_values, corpus, pension_rate, start_pension_year, end_pension_year, corpus_return_year):
    cash_flows = dict(zip(investment_years, investment_values))
    
    lump_sum = lump_sum_percentage * corpus
    annuity_corpus = corpus - lump_sum
    annual_pension = pension_rate * annuity_corpus
    
    # Add lump sum withdrawal in 2056
    cash_flows[2056] = lump_sum + annual_pension
    
    # Add pension payouts from 2056 to 2075
    for year in range(start_pension_year+1, end_pension_year + 1):
        cash_flows[year] = annual_pension
    
    # Add corpus return in 2076
    cash_flows[corpus_return_year] = annuity_corpus
    
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
corpus = 168773597
pension_rate = 0.067  # 6.7%
start_pension_year = 2056
end_pension_year = 2075
corpus_return_year = 2076
discount_rate = 0.08  # 7% discount rate

# Compute IRR for different withdrawal percentages
withdrawal_percentages = np.arange(0, 61, 5) / 100  # 0% to 60% in steps of 5%
irrs = [calculate_irr(wp, years, investments, corpus, pension_rate, start_pension_year, end_pension_year, corpus_return_year) for wp in withdrawal_percentages]
# Compute NPV for different withdrawal percentages
npvs = [calculate_npv(discount_rate, wp, years, investments, corpus, pension_rate, start_pension_year, end_pension_year, corpus_return_year) for wp in withdrawal_percentages]

# Plot results
plt.figure(figsize=(10, 5))
plt.plot(withdrawal_percentages * 100, np.array(irrs) * 100, marker='o', linestyle='-')
plt.xlabel("Lump Sum Withdrawal (%)")
plt.ylabel("IRR (%)")
plt.title("Impact of Lump Sum Withdrawal on IRR")
plt.grid()
plt.show()

# Plot NPV results
plt.figure(figsize=(10, 5))
plt.plot(withdrawal_percentages * 100, npvs, marker='s', linestyle='-', color='r', label='NPV')
plt.xlabel("Lump Sum Withdrawal (%)")
plt.ylabel("NPV(in crores)")
plt.ticklabel_format(style='sci', axis='y', scilimits=(7,7))  # Adjust scale

plt.title("Impact of Lump Sum Withdrawal on NPV")
plt.grid()
plt.legend()
plt.show()
