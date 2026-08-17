from datetime import datetime
from modelapp.models import CropField
from modelapp.growth import compute_growth


def _serialize(field: CropField):
    growth = compute_growth(field.planting_date)
    return {
        "id": field.id,
        "field_name": field.field_name,
        "variety": field.variety,
        "area_acres": field.area_acres,
        "planting_date": field.planting_date.isoformat(),
        **growth,
    }


def save_field(field_name: str, planting_date_str: str, variety: str = "", area_acres=None):
    planting_date = datetime.strptime(planting_date_str, "%Y-%m-%d").date()
    field = CropField.objects.create(
        field_name=field_name,
        variety=variety or "",
        area_acres=area_acres,
        planting_date=planting_date,
    )
    return _serialize(field)


def get_fields():
    return [_serialize(f) for f in CropField.objects.all()]


def get_field(field_id: int):
    field = CropField.objects.get(id=field_id)
    return _serialize(field)


def get_latest_field():
    field = CropField.objects.first()
    return _serialize(field) if field else None