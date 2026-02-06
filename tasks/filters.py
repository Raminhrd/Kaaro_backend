import django_filters
from tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    created_from = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_to = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Task
        fields = {
            "status": ["exact"],
            "service": ["exact"],
            "specialist": ["isnull"],  # specialist__isnull=true/false
        }