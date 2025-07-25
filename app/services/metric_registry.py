def get_metric(source: str | None, token: str) -> dict | None:
    metric = metric_registry.get(token)
    if not metric:
        return None
    if source and metric.get("statement") != source:
        return None
    return metric
def get_all_metrics(statement: str) -> list[str]:
    return [entry["column"] for entry in metric_registry.values() if entry["statement"] == statement]

def get_metric_map(statement: str) -> dict[str, str]:
    return {k: v["column"] for k, v in metric_registry.items() if v["statement"] == statement}

metric_registry ={
    "revenue": {
        "column": "revenue",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "costOfRevenue": {
        "column": "costOfRevenue",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "grossProfit": {
        "column": "grossProfit",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "researchAndDevelopmentExpenses": {
        "column": "researchAndDevelopmentExpenses",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "generalAndAdministrativeExpenses": {
        "column": "generalAndAdministrativeExpenses",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "sellingAndMarketingExpenses": {
        "column": "sellingAndMarketingExpenses",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "sellingGeneralAndAdministrativeExpenses": {
        "column": "sellingGeneralAndAdministrativeExpenses",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "otherExpenses": {
        "column": "otherExpenses",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "operatingExpenses": {
        "column": "operatingExpenses",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "costAndExpenses": {
        "column": "costAndExpenses",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "netInterestIncome": {
        "column": "netInterestIncome",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "interestIncome": {
        "column": "interestIncome",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "interestExpense": {
        "column": "interestExpense",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "depreciationAndAmortization": {
        "column": "depreciationAndAmortization",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "ebitda": {
        "column": "ebitda",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "ebit": {
        "column": "ebit",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "nonOperatingIncomeExcludingInterest": {
        "column": "nonOperatingIncomeExcludingInterest",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "operatingIncome": {
        "column": "operatingIncome",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "totalOtherIncomeExpensesNet": {
        "column": "totalOtherIncomeExpensesNet",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "incomeBeforeTax": {
        "column": "incomeBeforeTax",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "incomeTaxExpense": {
        "column": "incomeTaxExpense",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "netIncomeFromContinuingOperations": {
        "column": "netIncomeFromContinuingOperations",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "netIncomeFromDiscontinuedOperations": {
        "column": "netIncomeFromDiscontinuedOperations",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "otherAdjustmentsToNetIncome": {
        "column": "otherAdjustmentsToNetIncome",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "netIncome": {
        "column": "netIncome",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "netIncomeDeductions": {
        "column": "netIncomeDeductions",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "bottomLineNetIncome": {
        "column": "bottomLineNetIncome",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "eps": {
        "column": "eps",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "epsDiluted": {
        "column": "epsDiluted",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "weightedAverageShsOut": {
        "column": "weightedAverageShsOut",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "weightedAverageShsOutDil": {
        "column": "weightedAverageShsOutDil",
        "statement": "IS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "cashAndCashEquivalents": {
        "column": "cashAndCashEquivalents",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "shortTermInvestments": {
        "column": "shortTermInvestments",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "cashAndShortTermInvestments": {
        "column": "cashAndShortTermInvestments",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "netReceivables": {
        "column": "netReceivables",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "accountsReceivables": {
        "column": "accountsReceivables",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "otherReceivables": {
        "column": "otherReceivables",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "inventory": {
        "column": "inventory",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "prepaids": {
        "column": "prepaids",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "prepaidExpenses": {
        "column": "prepaidExpenses",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "otherCurrentAssets": {
        "column": "otherCurrentAssets",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "totalCurrentAssets": {
        "column": "totalCurrentAssets",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "propertyPlantEquipmentNet": {
        "column": "propertyPlantEquipmentNet",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "propertyPlantAndEquipmentNet": {
        "column": "propertyPlantAndEquipmentNet",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "goodwill": {
        "column": "goodwill",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "intangibleAssets": {
        "column": "intangibleAssets",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "goodwillAndIntangibleAssets": {
        "column": "goodwillAndIntangibleAssets",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "longTermInvestments": {
        "column": "longTermInvestments",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "taxAssets": {
        "column": "taxAssets",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "otherNonCurrentAssets": {
        "column": "otherNonCurrentAssets",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "totalNonCurrentAssets": {
        "column": "totalNonCurrentAssets",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "otherAssets": {
        "column": "otherAssets",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "totalAssets": {
        "column": "totalAssets",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "totalPayables": {
        "column": "totalPayables",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "accountPayables": {
        "column": "accountPayables",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "otherPayables": {
        "column": "otherPayables",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "accruedExpenses": {
        "column": "accruedExpenses",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "shortTermDebt": {
        "column": "shortTermDebt",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "capitalLeaseObligationsCurrent": {
        "column": "capitalLeaseObligationsCurrent",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "taxPayables": {
        "column": "taxPayables",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "deferredRevenue": {
        "column": "deferredRevenue",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "otherCurrentLiabilities": {
        "column": "otherCurrentLiabilities",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "totalCurrentLiabilities": {
        "column": "totalCurrentLiabilities",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "longTermDebt": {
        "column": "longTermDebt",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "deferredRevenueNonCurrent": {
        "column": "deferredRevenueNonCurrent",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "deferredTaxLiabilitiesNonCurrent": {
        "column": "deferredTaxLiabilitiesNonCurrent",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "otherNonCurrentLiabilities": {
        "column": "otherNonCurrentLiabilities",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "totalNonCurrentLiabilities": {
        "column": "totalNonCurrentLiabilities",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "otherLiabilities": {
        "column": "otherLiabilities",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "capitalLeaseObligations": {
        "column": "capitalLeaseObligations",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "totalLiabilities": {
        "column": "totalLiabilities",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "treasuryStock": {
        "column": "treasuryStock",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "preferredStock": {
        "column": "preferredStock",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "preferredStocks": {
        "column": "preferredStocks",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "commonStock": {
        "column": "commonStock",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "commonStocks": {
        "column": "commonStocks",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "retainedEarnings": {
        "column": "retainedEarnings",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "additionalPaidInCapital": {
        "column": "additionalPaidInCapital",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "accumulatedOtherComprehensiveIncomeLoss": {
        "column": "accumulatedOtherComprehensiveIncomeLoss",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "otherTotalStockholdersEquity": {
        "column": "otherTotalStockholdersEquity",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "totalStockholdersEquity": {
        "column": "totalStockholdersEquity",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "totalEquity": {
        "column": "totalEquity",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "minorityInterest": {
        "column": "minorityInterest",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "totalLiabilitiesAndTotalEquity": {
        "column": "totalLiabilitiesAndTotalEquity",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "totalInvestments": {
        "column": "totalInvestments",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "totalDebt": {
        "column": "totalDebt",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "netDebt": {
        "column": "netDebt",
        "statement": "BS",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "deferredIncomeTax": {
        "column": "deferredIncomeTax",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "stockBasedCompensation": {
        "column": "stockBasedCompensation",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "changeInWorkingCapital": {
        "column": "changeInWorkingCapital",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "accountsPayables": {
        "column": "accountsPayables",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "otherWorkingCapital": {
        "column": "otherWorkingCapital",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "otherNonCashItems": {
        "column": "otherNonCashItems",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "netCashProvidedByOperatingActivities": {
        "column": "netCashProvidedByOperatingActivities",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "investmentsInPropertyPlantAndEquipment": {
        "column": "investmentsInPropertyPlantAndEquipment",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "acquisitionsNet": {
        "column": "acquisitionsNet",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "purchasesOfInvestments": {
        "column": "purchasesOfInvestments",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "salesMaturitiesOfInvestments": {
        "column": "salesMaturitiesOfInvestments",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "otherInvestingActivities": {
        "column": "otherInvestingActivities",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "netCashProvidedByInvestingActivities": {
        "column": "netCashProvidedByInvestingActivities",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "netDebtIssuance": {
        "column": "netDebtIssuance",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "longTermNetDebtIssuance": {
        "column": "longTermNetDebtIssuance",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "shortTermNetDebtIssuance": {
        "column": "shortTermNetDebtIssuance",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "netStockIssuance": {
        "column": "netStockIssuance",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "netCommonStockIssuance": {
        "column": "netCommonStockIssuance",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "commonStockIssuance": {
        "column": "commonStockIssuance",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "commonStockRepurchased": {
        "column": "commonStockRepurchased",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "netPreferredStockIssuance": {
        "column": "netPreferredStockIssuance",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "netDividendsPaid": {
        "column": "netDividendsPaid",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "commonDividendsPaid": {
        "column": "commonDividendsPaid",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "preferredDividendsPaid": {
        "column": "preferredDividendsPaid",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "otherFinancingActivities": {
        "column": "otherFinancingActivities",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "netCashProvidedByFinancingActivities": {
        "column": "netCashProvidedByFinancingActivities",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "effectOfForexChangesOnCash": {
        "column": "effectOfForexChangesOnCash",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "netChangeInCash": {
        "column": "netChangeInCash",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "cashAtEndOfPeriod": {
        "column": "cashAtEndOfPeriod",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "cashAtBeginningOfPeriod": {
        "column": "cashAtBeginningOfPeriod",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "operatingCashFlow": {
        "column": "operatingCashFlow",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "capitalExpenditure": {
        "column": "capitalExpenditure",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "freeCashFlow": {
        "column": "freeCashFlow",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "incomeTaxesPaid": {
        "column": "incomeTaxesPaid",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "interestPaid": {
        "column": "interestPaid",
        "statement": "CF",
        "schema": "financial",
        "table": "financial_fact",
        "source": "financial"
    },
    "grossProfitMargin": {
        "column": "grossProfitMargin",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "ebitMargin": {
        "column": "ebitMargin",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "ebitdaMargin": {
        "column": "ebitdaMargin",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "operatingProfitMargin": {
        "column": "operatingProfitMargin",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "pretaxProfitMargin": {
        "column": "pretaxProfitMargin",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "continuousOperationsProfitMargin": {
        "column": "continuousOperationsProfitMargin",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "operatingProfitMarginFromContinuousOperations": {
        "column": "operatingProfitMarginFromContinuousOperations",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "netProfitMargin": {
        "column": "netProfitMargin",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "bottomLineProfitMargin": {
        "column": "bottomLineProfitMargin",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "receivablesTurnover": {
        "column": "receivablesTurnover",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "payablesTurnover": {
        "column": "payablesTurnover",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "inventoryTurnover": {
        "column": "inventoryTurnover",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "fixedAssetTurnover": {
        "column": "fixedAssetTurnover",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "assetTurnover": {
        "column": "assetTurnover",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "currentRatio": {
        "column": "currentRatio",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "quickRatio": {
        "column": "quickRatio",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "solvencyRatio": {
        "column": "solvencyRatio",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "cashRatio": {
        "column": "cashRatio",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "priceToEarningsRatio": {
        "column": "priceToEarningsRatio",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "priceToEarningsGrowthRatio": {
        "column": "priceToEarningsGrowthRatio",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "forwardPriceToEarningsGrowthRatio": {
        "column": "forwardPriceToEarningsGrowthRatio",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "priceToBookRatio": {
        "column": "priceToBookRatio",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "priceToSalesRatio": {
        "column": "priceToSalesRatio",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "priceToFreeCashFlowRatio": {
        "column": "priceToFreeCashFlowRatio",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "priceToOperatingCashFlowRatio": {
        "column": "priceToOperatingCashFlowRatio",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "debtToAssetsRatio": {
        "column": "debtToAssetsRatio",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "debtToEquityRatio": {
        "column": "debtToEquityRatio",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "debtToCapitalRatio": {
        "column": "debtToCapitalRatio",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "longTermDebtToCapitalRatio": {
        "column": "longTermDebtToCapitalRatio",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "financialLeverageRatio": {
        "column": "financialLeverageRatio",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "workingCapitalTurnoverRatio": {
        "column": "workingCapitalTurnoverRatio",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "operatingCashFlowRatio": {
        "column": "operatingCashFlowRatio",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "operatingCashFlowSalesRatio": {
        "column": "operatingCashFlowSalesRatio",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "freeCashFlowOperatingCashFlowRatio": {
        "column": "freeCashFlowOperatingCashFlowRatio",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "debtServiceCoverageRatio": {
        "column": "debtServiceCoverageRatio",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "interestCoverageRatio": {
        "column": "interestCoverageRatio",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "shortTermOperatingCashFlowCoverageRatio": {
        "column": "shortTermOperatingCashFlowCoverageRatio",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "operatingCashFlowCoverageRatio": {
        "column": "operatingCashFlowCoverageRatio",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "capitalExpenditureCoverageRatio": {
        "column": "capitalExpenditureCoverageRatio",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "dividendPaidAndCapexCoverageRatio": {
        "column": "dividendPaidAndCapexCoverageRatio",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "dividendPayoutRatio": {
        "column": "dividendPayoutRatio",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "dividendYield": {
        "column": "dividendYield",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "dividendYieldPercentage": {
        "column": "dividendYieldPercentage",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "revenuePerShare": {
        "column": "revenuePerShare",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "netIncomePerShare": {
        "column": "netIncomePerShare",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "interestDebtPerShare": {
        "column": "interestDebtPerShare",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "cashPerShare": {
        "column": "cashPerShare",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "bookValuePerShare": {
        "column": "bookValuePerShare",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "tangibleBookValuePerShare": {
        "column": "tangibleBookValuePerShare",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "shareholdersEquityPerShare": {
        "column": "shareholdersEquityPerShare",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "operatingCashFlowPerShare": {
        "column": "operatingCashFlowPerShare",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "capexPerShare": {
        "column": "capexPerShare",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "freeCashFlowPerShare": {
        "column": "freeCashFlowPerShare",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "netIncomePerEBT": {
        "column": "netIncomePerEBT",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "ebtPerEbit": {
        "column": "ebtPerEbit",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "ebitPerEbitda": {
        "column": "ebitPerEbitda",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "priceToFairValue": {
        "column": "priceToFairValue",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "debtToMarketCap": {
        "column": "debtToMarketCap",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "effectiveTaxRate": {
        "column": "effectiveTaxRate",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "enterpriseValueMultiple": {
        "column": "enterpriseValueMultiple",
        "statement": "RM",
        "schema": "financial",
        "table": "ratios",
        "source": "financial"
    },
    "marketCap": {
        "column": "marketCap",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "enterpriseValue": {
        "column": "enterpriseValue",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "evToSales": {
        "column": "evToSales",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "evToOperatingCashFlow": {
        "column": "evToOperatingCashFlow",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "evToFreeCashFlow": {
        "column": "evToFreeCashFlow",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "evToEBITDA": {
        "column": "evToEBITDA",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "netDebtToEBITDA": {
        "column": "netDebtToEBITDA",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "incomeQuality": {
        "column": "incomeQuality",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "grahamNumber": {
        "column": "grahamNumber",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "grahamNetNet": {
        "column": "grahamNetNet",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "taxBurden": {
        "column": "taxBurden",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "interestBurden": {
        "column": "interestBurden",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "workingCapital": {
        "column": "workingCapital",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "investedCapital": {
        "column": "investedCapital",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "returnOnAssets": {
        "column": "returnOnAssets",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "operatingReturnOnAssets": {
        "column": "operatingReturnOnAssets",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "returnOnTangibleAssets": {
        "column": "returnOnTangibleAssets",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "returnOnEquity": {
        "column": "returnOnEquity",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "returnOnInvestedCapital": {
        "column": "returnOnInvestedCapital",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "returnOnCapitalEmployed": {
        "column": "returnOnCapitalEmployed",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "earningsYield": {
        "column": "earningsYield",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "freeCashFlowYield": {
        "column": "freeCashFlowYield",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "capexToOperatingCashFlow": {
        "column": "capexToOperatingCashFlow",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "capexToDepreciation": {
        "column": "capexToDepreciation",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "capexToRevenue": {
        "column": "capexToRevenue",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "salesGeneralAndAdministrativeToRevenue": {
        "column": "salesGeneralAndAdministrativeToRevenue",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "researchAndDevelopementToRevenue": {
        "column": "researchAndDevelopementToRevenue",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "stockBasedCompensationToRevenue": {
        "column": "stockBasedCompensationToRevenue",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "intangiblesToTotalAssets": {
        "column": "intangiblesToTotalAssets",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "averageReceivables": {
        "column": "averageReceivables",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "averagePayables": {
        "column": "averagePayables",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "averageInventory": {
        "column": "averageInventory",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "daysOfSalesOutstanding": {
        "column": "daysOfSalesOutstanding",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "daysOfPayablesOutstanding": {
        "column": "daysOfPayablesOutstanding",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "daysOfInventoryOutstanding": {
        "column": "daysOfInventoryOutstanding",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "operatingCycle": {
        "column": "operatingCycle",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "cashConversionCycle": {
        "column": "cashConversionCycle",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "freeCashFlowToEquity": {
        "column": "freeCashFlowToEquity",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "freeCashFlowToFirm": {
        "column": "freeCashFlowToFirm",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "tangibleAssetValue": {
        "column": "tangibleAssetValue",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    },
    "netCurrentAssetValue": {
        "column": "netCurrentAssetValue",
        "statement": "KM",
        "schema": "financial",
        "table": "key_metrics",
        "source": "financial"
    }
}