from django.shortcuts import render
from django.db.models import Sum, Count, Avg
from .models import State, County, CountyResult

def index(request):
    states = (
        State.objects
        .annotate(
            counties_count=Count("counties", distinct=True),
            total_votes_sum=Sum("counties__results__total_votes"),
            current_votes_sum=Sum("counties__results__current_votes"),
            avg_percent=Avg("counties__results__percent"),
        )
        .order_by("name")
    )

    counties = County.objects.select_related("state").order_by("state__name", "name")

    results = (
        CountyResult.objects
        .select_related("county", "county__state")
        .order_by("county__state__name", "county__name")[:1000]
    )

    overall = CountyResult.objects.aggregate(
        total_votes_all=Sum("total_votes"),
        current_votes_all=Sum("current_votes"),
        avg_percent_all=Avg("percent"),
        rows_count=Count("id"),
    )

    context = {
        "states": states,
        "counties": counties,
        "results": results,
        "overall": overall,
    }
    return render(request, "index.html", context)
