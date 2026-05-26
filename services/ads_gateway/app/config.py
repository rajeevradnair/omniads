
import os


def get_campaign_service_url() -> str:
    return os.getenv("CAMPAIGN_SERVICE_URL", "http://campaign-service:8001")

def get_targeting_service_url() -> str:
    return os.getenv("TARGETING_SERVICE_URL", "http://targeting-service:8002")
