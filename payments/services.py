import requests
from django.conf import settings


class PaymentGatewayService:
    @staticmethod
    def send_payment(*, account_number, amount, currency, external_id, provider="azam", additional_properties=None):
        base_url = (settings.PYTHON_GATEWAY_URL or "").rstrip("/")
        if not base_url:
            return {"ok": False, "status": "config_missing", "message": "PYTHON_GATEWAY_URL is not configured"}
        payload = {
            "accountNumber": account_number,
            "amount": str(amount),
            "currency": currency,
            "externalId": external_id,
            "provider": provider,
            "additionalProperties": additional_properties or {},
        }
        headers = {"Content-Type": "application/json"}
        token = getattr(settings, "PAYMENT_API_TOKEN", "")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        try:
            response = requests.post(f"{base_url}/mno-checkout", json=payload, headers=headers, timeout=20)
        except requests.RequestException as exc:
            return {"ok": False, "status": "error", "message": str(exc)}
        try:
            data = response.json()
        except ValueError:
            data = {"raw": response.text}
        data["ok"] = response.ok
        data["http_status"] = response.status_code
        return data
