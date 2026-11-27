from django.conf import settings


class PaymentGatewayService:
    """Payment gateway integration is intentionally suspended.

    Set PAYMENT_GATEWAY_ENABLED=True and configure PYTHON_GATEWAY_URL when ready.
    """

    @staticmethod
    def send_payment(*, account_number, amount, currency, external_id, provider="manual", additional_properties=None):
        enabled = str(getattr(settings, "PAYMENT_GATEWAY_ENABLED", "False")).lower() in {"1", "true", "yes", "on"}
        if not enabled:
            return {
                "ok": False,
                "status": "suspended",
                "message": "Payment gateway is suspended. Configure and enable it before processing payments.",
            }
        base_url = (getattr(settings, "PYTHON_GATEWAY_URL", "") or "").rstrip("/")
        if not base_url:
            return {"ok": False, "status": "config_missing", "message": "PYTHON_GATEWAY_URL is not configured"}
        return {
            "ok": False,
            "status": "not_implemented",
            "message": "Gateway is enabled but provider adapter is not implemented in this build.",
        }
