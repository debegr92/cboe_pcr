from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from typing import Any

import pandas as pd
import requests

URL = "https://cdn.cboe.com/data/us/options/market_statistics/daily/DATE_daily_options"


@dataclass
class PutCallRatioRow:
    name: str
    value: str


@dataclass
class VolumeOiRow:
    name: str
    call: int
    put: int
    total: int


@dataclass
class PutCallRatios:
    ratios: list[PutCallRatioRow]
    sum_of_all_products: list[VolumeOiRow]
    index_options: list[VolumeOiRow]
    exchange_traded_products: list[VolumeOiRow]
    equity_options: list[VolumeOiRow]
    cboe_volatility_index_vix: list[VolumeOiRow]
    spx_spxw: list[VolumeOiRow]
    oex: list[VolumeOiRow]
    mrut: list[VolumeOiRow]
    mxea: list[VolumeOiRow]
    mxef: list[VolumeOiRow]
    mxacw: list[VolumeOiRow]
    mxwld: list[VolumeOiRow]
    mxusa: list[VolumeOiRow]
    cbtx: list[VolumeOiRow]
    mbtx: list[VolumeOiRow]
    speqx: list[VolumeOiRow]
    speqw: list[VolumeOiRow]
    mgtn: list[VolumeOiRow]
    mgtnw: list[VolumeOiRow]

    def dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(
            {"name": r.name, "value": float(r.value)} for r in self.ratios
        )

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> PutCallRatios:
        def rows(key: str) -> list[VolumeOiRow]:
            return [VolumeOiRow(**x) for x in data[key]]

        return cls(
            ratios=[PutCallRatioRow(**x) for x in data["ratios"]],
            sum_of_all_products=rows("SUM OF ALL PRODUCTS"),
            index_options=rows("INDEX OPTIONS"),
            exchange_traded_products=rows("EXCHANGE TRADED PRODUCTS"),
            equity_options=rows("EQUITY OPTIONS"),
            cboe_volatility_index_vix=rows("CBOE VOLATILITY INDEX (VIX)"),
            spx_spxw=rows("SPX + SPXW"),
            oex=rows("OEX"),
            mrut=rows("MRUT"),
            mxea=rows("MXEA"),
            mxef=rows("MXEF"),
            mxacw=rows("MXACW"),
            mxwld=rows("MXWLD"),
            mxusa=rows("MXUSA"),
            cbtx=rows("CBTX"),
            mbtx=rows("MBTX"),
            speqx=rows("SPEQX"),
            speqw=rows("SPEQW"),
            mgtn=rows("MGTN"),
            mgtnw=rows("MGTNW"),
        )


def get_put_call_ratios(fetch_date: date) -> PutCallRatios | None:
    try:
        url_with_date = URL.replace("DATE", fetch_date.isoformat())
        resp = requests.get(url_with_date)
        print(f"fetch {url_with_date} -> status={resp.status_code}")
        if resp.status_code == 200:
            return PutCallRatios.from_json(json.loads(resp.content))
    except Exception as e:
        print(e)
    return None
