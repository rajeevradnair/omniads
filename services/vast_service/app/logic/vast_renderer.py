from html import escape

from libs.contracts.vast import VastRenderRequest


def render_vast_xml(request: VastRenderRequest) -> str:
    """Render a simplified VAST XML document for a selected creative."""

    duration = _format_duration(request.duration_seconds)

    ad_title = escape(request.creative_name)
    advertiser_name = escape(request.advertiser_name)
    media_url = escape(request.media_url)

    impression_url = (
        "http://localhost:8000/api/v1/ads_gateway/events/impression"
        f"?request_id={request.request_id}"
        f"&trace_id={request.trace_id}"
        f"&decision_id={request.decision_id}"
        f"&campaign_id={request.campaign_id}"
        f"&creative_id={request.creative_id}"
    )

    click_url = (
        "http://localhost:8000/api/v1/ads_gateway/events/click"
        f"?request_id={request.request_id}"
        f"&trace_id={request.trace_id}"
        f"&decision_id={request.decision_id}"
        f"&campaign_id={request.campaign_id}"
        f"&creative_id={request.creative_id}"
    )

    vast_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<VAST version="3.0">
  <Ad id="{escape(request.creative_id)}">
    <InLine>
      <AdSystem>OmniAds</AdSystem>
      <AdTitle>{ad_title}</AdTitle>
      <Advertiser>{advertiser_name}</Advertiser>
      <Impression><![CDATA[{impression_url}]]></Impression>
      <Creatives>
        <Creative id="{escape(request.creative_id)}">
          <Linear>
            <Duration>{duration}</Duration>
            <TrackingEvents>
              <Tracking event="start"><![CDATA[{impression_url}&event=start]]></Tracking>
              <Tracking event="complete"><![CDATA[{impression_url}&event=complete]]></Tracking>
            </TrackingEvents>
            <VideoClicks>
              <ClickThrough><![CDATA[{click_url}]]></ClickThrough>
            </VideoClicks>
            <MediaFiles>
              <MediaFile delivery="progressive" type="video/mp4" width="1280" height="720">
                <![CDATA[{media_url}]]>
              </MediaFile>
            </MediaFiles>
          </Linear>
        </Creative>
      </Creatives>
    </InLine>
  </Ad>
</VAST>
"""
    return vast_xml


def _format_duration(duration_seconds: int) -> str:
    """Convert seconds into VAST HH:MM:SS duration format."""

    hours = duration_seconds // 3600
    remaining_seconds = duration_seconds % 3600
    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"