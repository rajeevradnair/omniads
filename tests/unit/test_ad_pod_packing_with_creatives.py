from libs.contracts.ranking import RankedCandidate
from services.ranking_service.app.logic.ad_pod_packer import pack_ad_pod


def test_pack_ninety_second_pod_with_thirty_and_fifteen_second_ads():
    ranked_candidates = [
        _ranked_candidate("camp_autosure", "creative_autosure_30s", 30, 1),
        _ranked_candidate("camp_fitpulse", "creative_fitpulse_30s", 30, 2),
        _ranked_candidate("camp_streamfuel", "creative_streamfuel_15s", 15, 3),
        _ranked_candidate("camp_quickcart", "creative_quickcart_15s", 15, 4),
    ]

    packed_pod = pack_ad_pod(
        ranked_candidates=ranked_candidates,
        target_duration_seconds=90,
    )

    assert packed_pod.filled_duration_seconds == 90
    assert packed_pod.remaining_duration_seconds == 0
    assert packed_pod.fill_rate == 1.0
    assert len(packed_pod.selected_ads) == 4
    assert packed_pod.reasons == ["POD_FILLED_EXACTLY"]


def _ranked_candidate(
    campaign_id: str,
    creative_id: str,
    duration_seconds: int,
    rank: int,
) -> RankedCandidate:
    return RankedCandidate(
        campaign_id=campaign_id,
        creative_id=creative_id,
        creative_name=creative_id,
        advertiser_name="Test Advertiser",
        media_url=f"http://localhost:9000/assets/ads/{creative_id}.mp4",
        duration_seconds=duration_seconds,
        base_bid_cpm_usd=10.0,
        pacing_multiplier=1.0,
        objective_weight=1.0,
        final_score=10.0,
        rank=rank,
        reasons=["TEST"],
    )