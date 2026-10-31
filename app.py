from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import random


payment_counts = {
    "approved": 0,
    "declined": 0,
    "failed": 0,
}


class PaymentHandler(BaseHTTPRequestHandler):
    def send_json(self, status_code, response, extra_headers=None):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")

        if extra_headers:
            for name, value in extra_headers.items():
                self.send_header(name, value)

        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def do_GET(self):
        if self.path == "/health":
            self.send_json(200, {
                "status": "ok",
                "service": "payment-simulator",
            })

        elif self.path == "/metrics":
            metrics = "\n".join([
                "# HELP payment_transactions_total Total simulated payments by status",
                "# TYPE payment_transactions_total counter",
                f'payment_transactions_total{{status="approved"}} {payment_counts["approved"]}',
                f'payment_transactions_total{{status="declined"}} {payment_counts["declined"]}',
                f'payment_transactions_total{{status="failed"}} {payment_counts["failed"]}',
                "",
            ])

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "text/plain; version=0.0.4; charset=utf-8",
            )
            self.end_headers()
            self.wfile.write(metrics.encode())

        elif self.path == "/payment":
            self.send_json(
                405,
                {"error": "Use POST /payment"},
                extra_headers={"Allow": "POST"},
            )

        else:
            self.send_json(404, {
                "error": "Try GET /health, GET /metrics, or POST /payment",
            })

    def do_POST(self):
        if self.path != "/payment":
            self.send_json(404, {"error": "Try POST /payment"})
            return

        outcome = random.choices(
            ["approved", "declined", "failed"],
            weights=[80, 15, 5],
        )[0]
        payment_id = random.randint(10000, 99999)
        payment_counts[outcome] += 1

        self.send_json(200, {
            "payment_id": payment_id,
            "status": outcome,
        })

        print(
            f"event=payment_processed "
            f"payment_id={payment_id} "
            f"status={outcome}",
            flush=True,
        )


def create_server(port=8000):
    # Listen on all interfaces so Docker can forward traffic to this app.
    return HTTPServer(("0.0.0.0", port), PaymentHandler)


if __name__ == "__main__":
    server = create_server()
    print("Payment simulator listening on port 8000")
    server.serve_forever()