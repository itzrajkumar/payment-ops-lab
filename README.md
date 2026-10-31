# Payment Operations Lab

A beginner DevOps and SRE project that simulates a payment service and monitors its operational behavior locally.

This project uses synthetic transactions only. It does not process real payments or use customer data.

## What it does

- Simulates payment outcomes: approved, declined, or failed
- Provides a health endpoint
- Logs each simulated payment
- Exposes payment outcome counters in Prometheus format
- Runs the simulator, Prometheus, and Grafana with Docker Compose
- Uses GitHub Actions to run automated tests on pushes and pull requests
- Includes a Grafana alert for a high simulated payment failure rate
- Demonstrates a simulated incident and recovery

## Demo

![Grafana dashboard during the simulated payment incident](assets/payment-incident-demo.gif)

## Architecture

```text
Client
  ├── Payment simulator: http://localhost:8000
  ├── Prometheus:         http://localhost:9090
  └── Grafana:            http://localhost:3000

Prometheus scrapes the simulator's /metrics endpoint.
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

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | [http://localhost:8000/health](http://localhost:8000/health) | Checks whether the simulator is responding |
| `POST` | `http://localhost:8000/payment` | Returns one simulated payment result |
| `GET` | [http://localhost:8000/metrics](http://localhost:8000/metrics) | Shows payment counters in Prometheus format |
| `GET` | [http://localhost:9090](http://localhost:9090) | Opens the Prometheus interface |
| `GET` | [http://localhost:3000](http://localhost:3000) | Opens the Grafana interface |

`POST /payment` creates a simulated payment. `GET /payment` is not allowed and returns **HTTP 405 Method Not Allowed**, with `Allow: POST`.

Payment results are randomly generated using an 80% approved, 15% declined, and 5% failed distribution.

To send one simulated payment from a terminal:

```bash
curl -i -X POST http://localhost:8000/payment
```

## Monitoring

Prometheus reads the simulator's `/metrics` endpoint every five seconds. Grafana uses Prometheus as its data source to display the payment counters.

Example Prometheus query for counts by outcome:

```promql
payment_transactions_total
```

Total simulated payments across all outcomes:

```promql
sum(payment_transactions_total)
```

Failed-outcome percentage over the last five minutes:

```promql
100 * sum(increase(payment_transactions_total{status="failed"}[5m]))
    / sum(increase(payment_transactions_total[5m]))
```

The payment counters are held in the simulator's memory and reset when the simulator restarts.

## Reliability target for this lab

- **SLI:** Percentage of simulated payment outcomes with status `failed` over a rolling five-minute window.
- **SLO:** Keep the failed-outcome rate at or below 5% during lab exercises with recent test traffic.
- **Alert:** Grafana fires when the five-minute failed-outcome rate stays above 10% for one minute. The rule is evaluated every 10 seconds.

These are learning values based on the simulator's normal 5% failure setting, not production financial-service standards. The SLI measures simulated outcomes, not service availability: the simulator returns HTTP 200 even when the outcome is `failed`.

A percentage cannot be calculated when there have been no recent transactions. Generate test traffic before evaluating the five-minute SLI.

To send 100 synthetic payment requests from a Mac terminal:

```bash
for i in {1..100}; do
  curl -s -X POST http://localhost:8000/payment > /dev/null
done
```

The alert state is visible in Grafana under **Alerting → Alert rules**. This local learning setup does not have an external notification contact point configured.

## Automated tests

Run the tests locally with:

```bash
python3 -m unittest -v
```

The tests check the health endpoint, a successful `POST /payment`, and that `GET /payment` returns HTTP 405 with `Allow: POST`.

GitHub Actions runs the same tests when code is pushed or a pull request is opened.

## Simulated incident review

**Scenario:** The simulator's payment weights were temporarily changed so every simulated payment failed.

**Impact:** Simulated payment requests returned failed outcomes. No real payments or customers were involved.

**Detection:** A Grafana alert detected that the failed-outcome rate exceeded the configured threshold.

**Investigation:** Prometheus metrics and application logs were used to confirm the failures.

**Recovery:** The normal payment weights were restored and the Docker Compose service was rebuilt.

**Follow-up:** Keep the dashboard and alert, and verify them after future changes.