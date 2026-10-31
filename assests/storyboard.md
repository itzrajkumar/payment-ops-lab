# Payment incident demo: GIF storyboard

`payment-incident-demo.gif` is a 24-second loop (1000×560, 10 fps) for LinkedIn and the README.
Everything shown is **synthetic data from a local simulation**. The alert measures *simulated payment outcomes*,
not real payment processing or service availability.

| Time | Show | Caption |
|---|---|---|
| 0–2s | Title card | Payment Operations Lab — local simulation using synthetic transactions |
| 2–5s | Grafana dashboard; alert is Normal | Baseline: payment simulator and monitoring are running |
| 5–8s | Second terminal sending `POST /payment` requests during the forced-failure exercise | Incident drill: simulated payment outcomes are failing |
| 8–11s | Prometheus query / graph showing the failed-outcome rate rising | Detection signal: failed-outcome rate exceeds the lab threshold |
| 11–14s | Grafana alert goes Pending, then Firing (time-lapse badge shown) | Alert fired after the condition persisted through its evaluation period |
| 14–17s | App logs showing `event=payment_processed` and `status=failed` | Investigation: confirm the failures in metrics and logs |
| 17–21s | Restore weights and rebuild, then the alert returns to Normal (time-lapse badge shown) | Recovery: restore normal simulation and confirm recovery |
| 21–24s | Final title card | Synthetic data only · Docker Compose · GitHub Actions · Prometheus · Grafana |

## Incident drill

For the incident scene the simulator is deliberately set to return failed outcomes
(the GIF shows `weights=[0, 0, 100]`). Afterward the code **must be restored to `weights=[80, 15, 5]`**
(approved / declined / failed), then rebuilt with `docker compose up -d --build`.

## Notes on how the GIF was made

- The GIF is an **illustrated re-creation** of the dashboard, terminal, and logs, not a screen recording.
  The waits are compressed on purpose: the alert goes Pending, then Firing, and a time-lapse badge marks the skipped evaluation period.
- Values that are illustrative and should be matched to the real project before publishing:
  - the PromQL query `rate(payments_total{status="failed"}[1m])` (metric and label names)
  - the request line `POST /payment -> {"status": "failed"}`
  - the code context around `weights=` in `app.py`
  - the counter totals and the unlabeled "lab threshold" line
- To use real footage instead, record these same scenes at the same timings and keep the captions above.
