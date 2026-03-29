from datetime import date

from put_call_ratios import get_put_call_ratios

fetch_date = date(2026, 3, 27)
pcr = get_put_call_ratios(fetch_date)

if pcr is not None:
    print(f"\nPut/Call ratios for {fetch_date.isoformat()}:\n")
    print(pcr.dataframe())
