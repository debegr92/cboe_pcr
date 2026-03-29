from datetime import date

from put_call_ratios import get_put_call_ratios

pcr = get_put_call_ratios(date(2026, 3, 27))

print(pcr)
if pcr is not None:
    print(pcr.dataframe())
