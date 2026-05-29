from libs.contracts.ranking import PackedAdPod, RankedCandidate


def pack_ad_pod(
    ranked_candidates: list[RankedCandidate],
    target_duration_seconds: int,
) -> PackedAdPod:
    """Pack ranked candidates into a duration-constrained ad pod."""

    selected_ads: list[RankedCandidate] = []
    remaining_duration = target_duration_seconds

    for candidate in ranked_candidates:
        if candidate.duration_seconds <= remaining_duration:
            selected_ads.append(candidate)
            remaining_duration -= candidate.duration_seconds

        if remaining_duration == 0:
            break

    filled_duration = target_duration_seconds - remaining_duration

    fill_rate = (
        filled_duration / target_duration_seconds
        if target_duration_seconds > 0
        else 0.0
    )

    return PackedAdPod(
        selected_ads=selected_ads,
        target_duration_seconds=target_duration_seconds,
        filled_duration_seconds=filled_duration,
        remaining_duration_seconds=remaining_duration,
        fill_rate=round(fill_rate, 4),
        reasons=_build_pod_reasons(
            filled_duration_seconds=filled_duration,
            remaining_duration_seconds=remaining_duration,
        ),
    )


def _build_pod_reasons(
    filled_duration_seconds: int,
    remaining_duration_seconds: int,
) -> list[str]:
    """Return reason codes explaining the pod packing result."""

    if remaining_duration_seconds == 0:
        return ["POD_FILLED_EXACTLY"]

    if filled_duration_seconds == 0:
        return ["NO_ADS_FIT_POD"]

    return ["POD_PARTIALLY_FILLED"]