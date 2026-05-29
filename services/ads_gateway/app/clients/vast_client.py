import httpx

from libs.contracts.vast import VastRenderRequest, VastRenderResponse
from libs.contracts.vast import VastPodRenderRequest, VastPodRenderResponse

class VastServiceClient:
    """HTTP client for talking to VAST Service."""

    def __init__(self, base_url: str, timeout_seconds: float = 2.0):
        """Initialize the VAST Service client."""

        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def render_vast(self, request: VastRenderRequest) -> VastRenderResponse:
        """Render VAST XML for a selected creative."""

        url = f"{self.base_url}/api/v1/vast/render"

        response = httpx.post(
            url,
            json=request.model_dump(),
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()

        return VastRenderResponse(**response.json())
    
    def render_vast_pod(
        self,
        request: VastPodRenderRequest,
    ) -> VastPodRenderResponse:
        """Render VAST XML for a packed ad pod."""

        url = f"{self.base_url}/api/v1/vast/render_pod"

        response = httpx.post(
            url,
            json=request.model_dump(),
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()

        return VastPodRenderResponse(**response.json())