import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .services import scan_service, crop_growth_service
from .models import CropField

@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@login_required
def predict(request):
    return render(request, 'system/predict.html')

@login_required
def history(request):
    return render(request, 'system/history.html')

@login_required
def growth(request):
    return render(request, 'system/growth.html')

@csrf_exempt
@require_POST
def api_save_scan(request):
    body = json.loads(request.body)
    doc = scan_service.save_scan(
        raw_label=body["raw_label"],
        confidence=float(body["confidence"]),
        thumbnail_data_url=body.get("image_thumbnail", ""),
    )
    return JsonResponse(doc)

@require_GET
def api_summary(request):
    return JsonResponse(scan_service.get_summary())

@require_GET
def api_recent(request):
    limit = int(request.GET.get("limit", 8))
    return JsonResponse(scan_service.get_recent(limit), safe=False)

@require_GET
def api_history(request):
    date_str = request.GET.get("date")
    limit = int(request.GET.get("limit", 500))
    return JsonResponse(scan_service.get_history(date_str, limit), safe=False)

@require_GET
def api_trend(request):
    return JsonResponse(scan_service.get_trend(), safe=False)

@require_GET
def api_class_distribution(request):
    return JsonResponse(scan_service.get_class_distribution())

@csrf_exempt
@require_POST
def api_save_field(request):
    body = json.loads(request.body)
    doc = crop_growth_service.save_field(
        field_name=body["field_name"],
        planting_date_str=body["planting_date"],
        variety=body.get("variety", ""),
        area_acres=body.get("area_acres"),
    )
    return JsonResponse(doc)

@require_GET
def api_fields(request):
    return JsonResponse(crop_growth_service.get_fields(), safe=False)

@require_GET
def api_field_detail(request, field_id):
    try:
        return JsonResponse(crop_growth_service.get_field(field_id))
    except CropField.DoesNotExist:
        return JsonResponse({"error": "Field not found"}, status=404)

@require_GET
def api_latest_field(request):
    doc = crop_growth_service.get_latest_field()
    return JsonResponse(doc or {})