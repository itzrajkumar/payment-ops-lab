# Payment Operations Lab

A beginner DevOps and SRE project that simulates a payment service and monitors its operational behavior locally.

This project uses fake transactions only. It does not process real payments or use customer data.

## What it does

- Returns simulated payment outcomes: approved, declined, or failed
- Provides a health endpoint
- Writes a log entry for each simulated payment
- Exposes payment outcome counters in Prometheus format
- Runs in Docker Compose with Prometheus and Grafana
- Uses GitHub Actions to run automated tests

## Architecture

```text
Browser
  ├── Payment simulator: http://localhost:8000
  ├── Prometheus:         http://localhost:9090
  └── Grafana:            http://localhost:3000

Prometheus scrapes the payment simulator's /metrics endpoint.
Grafana queries Prometheus and displays the metrics.
```

## Requirements

- Docker Desktop
- Git

The payment simulator uses Python's standard library.

## Start the project

From the project directory, run:

```bash
docker compose up --build
```

This builds the payment simulator image and starts the payment simulator, Prometheus, and Grafana.

To stop the services, press **Control+C**. If needed, run:

```bash
docker compose down
```

## Service endpoints

| Endpoint | Purpose |
|---|---|
| [http://localhost:8000/health](http://localhost:8000/health) | Checks whether the simulator is responding |
| [http://localhost:8000/payment](http://localhost:8000/payment) | Returns one fake payment result |
| [http://localhost:8000/metrics](http://localhost:8000/metrics) | Shows payment counters in Prometheus format |
| [http://localhost:9090](http://localhost:9090) | Opens the Prometheus interface |
| [http://localhost:3000](http://localhost:3000) | Opens the Grafana interface |

Payment results are randomly generated using an 80% approved, 15% declined, and 5% failed distribution.

## Monitoring

Prometheus reads the simulator's `/metrics` endpoint every five seconds. Grafana uses Prometheus as its data source to display the payment counters.

Example Prometheus query for payment counts by outcome:

```promql
payment_transactions_total
```

Total simulated payments across all outcomes:

```promql
sum(payment_transactions_total)
```

Failed payments detected in the last minute:

```promql
increase(payment_transactions_total{status="failed"}[1m])
```

The payment counters are held in the simulator's memory and reset when the simulator restarts.

The Grafana alert rule monitors failed payments. Its state can be viewed in Grafana under **Alerting → Alert rules**. This local learning setup does not have an external notification contact point configured.

## Reliability target for this lab

**SLI:** The percentage of simulated payment outcomes with status `failed` in a rolling five-minute window.

**SLO:** For this learning project, keep the failed-outcome rate at or below 5% over that window when there is enough test traffic. This is a lab target based on the simulator's normal 5% failure setting, not a production standard.

Prometheus query for the failed-outcome rate as a percentage:

```promql
100 * sum(increase(payment_transactions_total{status="failed"}[5m]))
    / sum(increase(payment_transactions_total[5m]))



SLI: Percentage of simulated payment outcomes marked failed over a rolling five-minute window.

SLO: Keep that rate at or below 5% during lab exercises with recent test traffic.

Alert: Grafana fires when the rate stays above 10% for one minute.

Query:
100 * sum(increase(payment_transactions_total{status="failed"}[5m]))
    / sum(increase(payment_transactions_total[5m]))

his measures simulated payment outcomes, not service availability. The simulator returns HTTP 200 even when an outcome is failed. With no recent requests, the percentage can be undefined, so generate test traffic before evaluating it.

## Automated tests

Run the tests locally with:

```bash
python3 -m unittest -v
```

GitHub Actions runs the same tests when code is pushed or a pull request is opened.

## Simulated incident review

**Scenario:** The simulator's payment weights were temporarily changed so every simulated payment failed.

**Impact:** Simulated payments returned failed outcomes. No real payments or customers were involved.

**Detection:** A Grafana alert watched the failed-payment metric and changed state when failures increased.

**Investigation:** The payment metrics and application logs were used to confirm the failed outcomes.

**Recovery:** The normal payment weights were restored and the Docker Compose service was rebuilt.

**Follow-up:** Keep the alert and dashboard, and verify them after future changes.