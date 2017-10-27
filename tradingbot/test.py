import support
print support.get_nonzero_balances()
non_zeros_balances = support.get_nonzero_balances()
print non_zeros_balances
for el in non_zeros_balances.keys():
     print non_zeros_balances.get(el)* float(support.get_data(
         "/exchange/ticker",
                                         [("currencyPair", el)])["best_bid"])