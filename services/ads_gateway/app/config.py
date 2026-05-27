
import os


def get_campaign_service_url() -> str:
    return os.getenv("CAMPAIGN_SERVICE_URL", "http://campaign-service:8001")

def get_targeting_service_url() -> str:
    return os.getenv("TARGETING_SERVICE_URL", "http://targeting-service:8002")

def get_vast_service_url() -> str:
    return os.getenv("VAST_SERVICE_URL", "http://vast-service:8003")

def get_candidate_service_url() -> str:
    return os.getenv("CANDIDATE_SERVICE_URL", "http://candidate-service:8004")

def get_frequency_cap_service_url() -> str:
    return os.getenv("FREQUENCY_CAP_SERVICE_URL","http://frequency-cap-service:8005")