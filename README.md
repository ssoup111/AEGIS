# AI Trading Lab / Project AEGIS v0.2

Multi-agent stock scanning system.

Current features:
- Real market data through yfinance
- Watchlist scanner
- Plug-in style agent registry
- Multi-agent scoring
- CIO ranking
- Automatic JSONL decision logging
- Mission Control dashboard
- Paper-trading text reports
- Optional email delivery for generated reports

Run:
```bash
source .venv/bin/activate
python main.py
```

Generate the latest paper-trading report:
```bash
python3 -m aegis.reports
```

Email the latest report:
```bash
export AEGIS_EMAIL_TO="recipient@example.com"
export AEGIS_EMAIL_FROM="your-gmail-address@gmail.com"
export AEGIS_EMAIL_APP_PASSWORD="your-gmail-app-password"
python3 -m aegis.emailer
```

Email delivery uses `reports/latest_report.txt`. If the report does not exist, run
`python3 -m aegis.reports` first.

The emailer uses only environment variables for credentials. It does not send
anything when required variables are missing, and it does not connect Alpaca or
place trades.
