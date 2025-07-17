# app/services/prompt_utils.py

from app.constants.metrics import RATIOS_METRICS, KEY_METRICS

# Set of raw metric names that should be displayed as percentages
RATIO_METRICS = set(RATIOS_METRICS.values())
VALUATION_PERCENT_METRICS = {
    "returnOnAssets",
    "returnOnEquity",
    "returnOnCapitalEmployed",
    "returnOnInvestedCapital",
    "returnOnTangibleAssets",
    "dividendYield",
    "dividendYieldPercentage",
    "dividendPayoutRatio",
    "effectiveTaxRate",
    "capexToRevenue",
    "capexToOperatingCashFlow",
    "capexToDepreciation",
    "salesGeneralAndAdministrativeToRevenue",
    "stockBasedCompensationToRevenue",
    "researchAndDevelopementToRevenue",
    "intangiblesToTotalAssets",
    "incomeQuality",
    "taxBurden",
    "interestBurden",
    "earningsYield",
    "freeCashFlowYield"
}

PERCENTAGE_METRICS = RATIO_METRICS.union(VALUATION_PERCENT_METRICS)


def get_value_type(metric_id: str) -> str:
    # Normalize: lowercase + remove underscores
    normalized_id = metric_id.strip().lower().replace("_", "")

    ratio_metrics = {v.lower().replace("_", "") for v in RATIOS_METRICS.values()}
    valuation_percent_metrics = {v.lower().replace("_", "") for v in VALUATION_PERCENT_METRICS}

    # These ratios are plain (not dollar or percent)
    plain_ratio_metrics = {
        "currentratio",
        "quickratio",
        "cashratio",
        "financialleverageratio",
        "debttoequityratio",
        "debttoassetsratio",
        "debttocapitalratio",
        "longtermdebttocapitalratio",
        "interestratiocoverage",
        "enterprisemultiple",
        "workingcapitalturnoverratio",
        "operatingcashflowratio",
        "operatingcashflowsalesratio",
        "shorttermoperatingcashflowcoverageratio",
        "operatingcashflowcoverageratio",
        "capitalexpenditurecoverageratio",
        "dividendpaidandcapexcoverageratio",
    }

    if normalized_id in valuation_percent_metrics:
        return "percent"
    elif normalized_id in plain_ratio_metrics or normalized_id in ratio_metrics:
        return "plain"
    else:
        print(f"[DEBUG] Unknown metric type for '{metric_id}' → normalized: '{normalized_id}' (defaulting to 'dollar')")
        return "dollar"
