import streamlit_shadcn_ui as ui
import streamlit as st
import requests

api_key = "e3e1ef68f4575bca8a430996a4e11ed1"


def get_exchange_rate(from_currency, date, to_currency="USD"):
    url = f"https://financialmodelingprep.com/api/v3/historical-chart/4hour/{from_currency}{to_currency}?from={date}&to={date}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    if not data:
        return 1  # Default to 1 if no data found

    exchange_rate = data[0].get('close', 1)
    return exchange_rate


def safe_division(numerator, denominator):
    return numerator / denominator if denominator != 0 else 0


def ratio_indicator(current_ratio, average_current_ratio, cash_equivalents, reportedCurrency, longTermDebt, Share_Issued, fillingDate,
                    totalLiabilities, totalAssets, average_debt_ratio):
    Net_cash_share = safe_division(cash_equivalents - longTermDebt, Share_Issued)

    if reportedCurrency != "USD":
        exchange_rate = get_exchange_rate(reportedCurrency, date=fillingDate)
    else:
        exchange_rate = 1

    exchange_rate = float(exchange_rate)
    Net_cash_share = float(Net_cash_share)
    Net_cash_share = Net_cash_share * exchange_rate
    debt_ratio = safe_division(totalLiabilities, totalAssets)

    # Display
    cols = st.columns(3)
    with cols[0]:
        ui.metric_card(
            title="Current_ratio:",
            content=f"{current_ratio}",
            key="Current_ratio",
        )
        ui.badges(
            badge_list=[(f"Average: {average_current_ratio}", "default")],
            class_name="flex gap-3",
            key="average_current_ratio_badges"
        )
    with cols[1]:
        ui.metric_card(
            title="Net cash per share:",
            content=f"{Net_cash_share:.2f}",
            key="Net cash per share:",
        )
    with cols[2]:
        ui.metric_card(
            title="Debt Ratio:",
            content=f"{debt_ratio:.2f}",
            key="Debt factor",
        )
        ui.badges(
            badge_list=[(f"Average: {average_debt_ratio:.2f}", "default")],
            class_name="flex gap-3",
            key="average_debt_ratio_badges"
        )


def ratio_indicator_2(cashAndCashEquivalents, totalCurrentLiabilities, netReceivables, average_quick_ratio, ttm_operating_income,
                      ttm_revenue, ttm_totalOtherIncomeExpensesNet, totalAssets, ttm_net_income, average_operation_margin, roa, average_pre_tax):

    quick_ratio = safe_division(cashAndCashEquivalents + netReceivables, totalCurrentLiabilities)
    operation_margin = safe_division(ttm_operating_income, ttm_revenue) * 100
    pre_tax_margin = safe_division(ttm_operating_income + ttm_totalOtherIncomeExpensesNet, ttm_revenue) * 100
    return_on_assets = safe_division(ttm_net_income, totalAssets) * 100

    cols = st.columns(2)
    with cols[0]:
        ui.metric_card(
            title="Quick Ratio:",
            content=f"{quick_ratio:.2f}",
            key="Quick_ratio",
        )
        ui.badges(
            badge_list=[(f"Average: {average_quick_ratio:.2f}", "default")],
            class_name="flex gap-3",
            key="average_quick_ratio_badges"
        )
        ui.metric_card(
            title="Pre-tax Margin:",
            content=f"{pre_tax_margin:.2f}%",
            key="Pre-tax Margin",
        )
        ui.badges(
            badge_list=[(f"Average: {average_pre_tax}%", "default")],
            class_name="flex gap-3",
            key="average_pre_tax_badges"
        )
    with cols[1]:
        ui.metric_card(
            title="Operation Margin:",
            content=f"{operation_margin:.2f}%",
            key="Operation Margin",
        )
        ui.badges(
            badge_list=[(f"Average: {(average_operation_margin*100):.1f}%", "default")],
            class_name="flex gap-3",
            key="average_operation_margin_badges"
        )
        ui.metric_card(
            title="Return on Assets:",
            content=f"{return_on_assets:.2f}%",
            key="Return on Assets",
        )
        ui.badges(
            badge_list=[(f"Average: {(roa)}%", "default")],
            class_name="flex gap-3",
            key="average_roa_badges"
        )