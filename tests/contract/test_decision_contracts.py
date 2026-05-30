from libs.contracts.ad_request import AdDecisionRequest
from libs.contracts.candidate import CandidateGenerationRequest
from libs.contracts.campaign import ActiveCampaign
from libs.contracts.ranking import RankedCandidate, PackedAdPod
from libs.contracts.vast import VastPodRenderRequest


def test_candidate_generation_contract_serializes():
    ad_request = _ad_request()
    campaign = _active_campaign()

    request = CandidateGenerationRequest(
        ad_request=ad_request,
        active_campaigns=[campaign],
        max_candidates=4,
    )

    payload = request.model_dump()

    assert payload["ad_request"]["viewer_id"] == "viewer_contract_test"
    assert payload["active_campaigns"][0]["campaign_id"] == "camp_test"


def test_packed_ad_pod_contract_serializes():
    ranked = _ranked_candidate()

    pod = PackedAdPod(
        selected_ads=[ranked],
        target_duration_seconds=90,
        filled_duration_seconds=30,
        remaining_duration_seconds=60,
        fill_rate=0.3333,
        reasons=["POD_PARTIALLY_FILLED"],
    )

    payload = pod.model_dump()

    assert payload["selected_ads"][0]["creative_id"] == "creative_test"
    assert payload["target_duration_seconds"] == 90


def test_vast_pod_render_contract_serializes():
    ranked = _ranked_candidate()

    request = VastPodRenderRequest(
        request_id="req_test",
        trace_id="trace_test",
        decision_id="decision_test",
        selected_ads=[ranked],
    )

    payload = request.model_dump()

    assert payload["selected_ads"][0]["media_url"].endswith(".mp4")


def _ad_request() -> AdDecisionRequest:
    return AdDecisionRequest(
        viewer_id="viewer_contract_test",
        session_id="session_contract_test",
        content_id="content_sports_001",
        placement_id="sports_midroll_001",
        ad_break_id="break_001",
        device="ctv",
        geo="CA",
    )


def _active_campaign() -> ActiveCampaign:
    return ActiveCampaign(
        campaign_id="camp_test",
        campaign_name="Test Campaign",
        advertiser_id="adv_test",
        advertiser_name="Test Advertiser",
        objective="CONVERSION",
        daily_budget_usd=1000.0,
        base_bid_cpm_usd=12.0,
        creative_id="creative_test",
        creative_name="Test Creative",
        media_url="http://localhost:9000/assets/ads/test.mp4",
        duration_seconds=30,
        placement_id="sports_midroll_001",
    )


def _ranked_candidate() -> RankedCandidate:
    return RankedCandidate(
        campaign_id="camp_test",
        creative_id="creative_test",
        creative_name="Test Creative",
        advertiser_name="Test Advertiser",
        media_url="http://localhost:9000/assets/ads/test.mp4",
        duration_seconds=30,
        base_bid_cpm_usd=12.0,
        pacing_multiplier=1.0,
        objective_weight=1.2,
        final_score=14.4,
        rank=1,
        reasons=["TEST_REASON"],
    )