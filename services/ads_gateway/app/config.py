
import os


def get_campaign_service_url() -> str:
    return os.getenv("CAMPAIGN_SERVICE_URL", "http://campaign-service:8001")