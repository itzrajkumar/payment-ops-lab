from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import random


class PaymentHandler(BaseHTTPRequestHandler):
    def send_json(self, status_code, response):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def do_GET(self):
        if self.path == "/health":
            self.send_json(200, {
                "status": "ok",
                "service": "payment-simulator"
            })
        elif self.path == "/payment":
            outcome = random.choices(
                ["approved", "declined", "failed"],
                weights=[80, 15, 5]
            )[0]
            self.send_json(200, {
                "payment_id": random.randint(10000, 99999),
                "status": outcome
            })
        else:
            self.send_json(404, {"error": "Try /health or /payment"})


def create_server(port=8000):
    return HTTPServer(("127.0.0.1", port), PaymentHandler)


if __name__ == "__main__":
    server = create_server()
    print("Payment simulator listening on port 8000")
    server.serve_forever()