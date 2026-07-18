import os
import re
from datetime import datetime

from dotenv import load_dotenv
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.enums import DataFeed

from config import TIMEFRAME, SYMBOL, START_DATE, END_DATE

load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

TIMEFRAME_UNITS = {
    "min": TimeFrameUnit.Minute,
    "h": TimeFrameUnit.Hour,
    "d": TimeFrameUnit.Day,
}


def parse_timeframe(value: str) -> TimeFrame:

    match = re.fullmatch(r"(\d+)(min|h|d)", value.strip().lower())
    if not match:
        raise ValueError(f"TIMEFRAME inválido: {value!r}")
    amount, unit = match.groups()
    return TimeFrame(int(amount), TIMEFRAME_UNITS[unit])


def main():
    client = StockHistoricalDataClient(API_KEY, SECRET_KEY)

    request = StockBarsRequest(
        symbol_or_symbols=SYMBOL,
        timeframe=parse_timeframe(TIMEFRAME),
        start=datetime.strptime(START_DATE, "%Y-%m-%d"),
        end=datetime.strptime(END_DATE, "%Y-%m-%d"),
        feed=DataFeed.IEX,
    )

    bars = client.get_stock_bars(request).df

    os.makedirs("data", exist_ok=True)
    output_path = os.path.join("data", f"{SYMBOL}_{TIMEFRAME}_{START_DATE}_{END_DATE}.csv")
    bars.to_csv(output_path)
    print(f"Guardado en {output_path}")


if __name__ == "__main__":
    main()
