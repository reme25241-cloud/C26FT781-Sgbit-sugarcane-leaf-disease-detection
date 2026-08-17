from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Count
from modelapp.models import Scan
from modelapp.labels import get_label_info, ALL_CLASS_KEYS, LABEL_INFO


def _serialize(scan: Scan):
    return {
        "_id": str(scan.id),
        "disease_class": scan.disease_class,
        "class_key": scan.class_key,
        "severity": scan.severity,
        "recommendation": scan.recommendation,
        "confidence": scan.confidence,
        "image_thumbnail": scan.image_thumbnail,
        "timestamp": scan.timestamp.isoformat(),
    }


def save_scan(raw_label: str, confidence: float, thumbnail_data_url: str):
    info = get_label_info(raw_label)
    scan = Scan.objects.create(
        disease_class=info["display"],
        class_key=info["key"],
        severity=info["severity"],
        recommendation=info["recommendation"],
        confidence=confidence,
        image_thumbnail=thumbnail_data_url,
    )
    return _serialize(scan)


def get_recent(limit=8):
    return [_serialize(s) for s in Scan.objects.all()[:limit]]


def get_history(date_str=None, limit=500):
    qs = Scan.objects.all()
    if date_str:
        day = datetime.strptime(date_str, "%Y-%m-%d").date()
        qs = qs.filter(timestamp__date=day)
    return [_serialize(s) for s in qs[:limit]]


def _class_distribution():
    dist = {k: 0 for k in ALL_CLASS_KEYS}
    for row in Scan.objects.values("class_key").annotate(count=Count("class_key")):
        if row["class_key"] in dist:
            dist[row["class_key"]] = row["count"]
    return dist


def get_class_distribution():
    return _class_distribution()


def get_suggestions(dist: dict, total: int):
    """Generate simple actionable suggestions based on current class distribution."""
    if total == 0:
        return ["No scans recorded yet. Start scanning leaves to get insights."]

    suggestions = []
    key_to_info = {v["key"]: v for v in LABEL_INFO.values()}

    for key, count in dist.items():
        if key == "healthy" or count == 0:
            continue
        share = count / total
        info = key_to_info.get(key)
        if info and share >= 0.25:
            suggestions.append(
                f"{info['display']} accounts for {share*100:.0f}% of scans — {info['recommendation']}"
            )

    healthy_share = dist.get("healthy", 0) / total
    if healthy_share >= 0.8:
        suggestions.append("Field looks healthy overall. Maintain current monitoring schedule.")
    elif not suggestions:
        suggestions.append("Disease presence is mixed and low-severity. Keep monitoring regularly.")

    return suggestions[:5]


def _pct_change(current: float, previous: float):
    """Percentage change from previous -> current. None if previous has no baseline."""
    if previous == 0:
        return None if current == 0 else 100.0
    return ((current - previous) / previous) * 100


def get_growth_rate():
    """
    Compares this week (last 7 days, including today) vs the prior 7-day window,
    for both total scan volume and disease rate.
    """
    now = timezone.now()
    today = now.date()

    this_week_start = today - timedelta(days=6)
    prev_week_start = today - timedelta(days=13)
    prev_week_end = today - timedelta(days=7)

    this_week_qs = Scan.objects.filter(timestamp__date__gte=this_week_start, timestamp__date__lte=today)
    prev_week_qs = Scan.objects.filter(timestamp__date__gte=prev_week_start, timestamp__date__lte=prev_week_end)

    this_week_total = this_week_qs.count()
    prev_week_total = prev_week_qs.count()

    this_week_diseased = this_week_qs.exclude(class_key="healthy").count()
    prev_week_diseased = prev_week_qs.exclude(class_key="healthy").count()

    this_week_rate = (this_week_diseased / this_week_total * 100) if this_week_total else 0.0
    prev_week_rate = (prev_week_diseased / prev_week_total * 100) if prev_week_total else 0.0

    return {
        "scan_volume_growth": _pct_change(this_week_total, prev_week_total),
        "disease_rate_growth": _pct_change(this_week_rate, prev_week_rate),
        "this_week_scans": this_week_total,
        "prev_week_scans": prev_week_total,
        "this_week_disease_rate": round(this_week_rate, 1),
        "prev_week_disease_rate": round(prev_week_rate, 1),
    }


def get_summary():
    total = Scan.objects.count()
    healthy = Scan.objects.filter(class_key="healthy").count()
    diseased = total - healthy
    avg_conf = 0.0
    confidences = list(Scan.objects.values_list("confidence", flat=True))
    if confidences:
        avg_conf = sum(confidences) / len(confidences)

    weekly = []
    for i in range(6, -1, -1):
        day = (timezone.now() - timedelta(days=i)).date()
        day_qs = Scan.objects.filter(timestamp__date=day)
        weekly.append({
            "day": day.strftime("%a"),
            "healthy": day_qs.filter(class_key="healthy").count(),
            "diseased": day_qs.exclude(class_key="healthy").count(),
        })

    dist = _class_distribution()

    return {
        "total_scans": total,
        "healthy_count": healthy,
        "diseased_count": diseased,
        "avg_confidence": avg_conf,
        "weekly": weekly,
        "class_distribution": dist,
        "suggestions": get_suggestions(dist, total),
        "growth": get_growth_rate(),
    }


def get_trend(days=14):
    trend = []
    for i in range(days - 1, -1, -1):
        day = (timezone.now() - timedelta(days=i)).date()
        count = Scan.objects.filter(timestamp__date=day).count()
        trend.append({"day": day.strftime("%b %d"), "count": count})
    return trend