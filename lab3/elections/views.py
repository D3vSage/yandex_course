from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Count, Avg
from .models import State, County, CountyResult
from .forms import CountyForm

TABLE_LIMIT = 20

def index(request):
    if request.method == "POST":
        delete_id = request.POST.get("delete_id")
        if delete_id:
            county = get_object_or_404(County, pk=delete_id)
            county.delete()
            return redirect("index")

        county_id = request.POST.get("county_id") 
        if county_id:
            county = get_object_or_404(County, pk=county_id)
            form = CountyForm(request.POST, instance=county)
        else:
            form = CountyForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("index")

        edit_mode = True if county_id else False
        editing_county = get_object_or_404(County, pk=county_id) if county_id else None

    else:
        edit_id = request.GET.get("edit")
        if edit_id:
            editing_county = get_object_or_404(County, pk=edit_id)
            form = CountyForm(instance=editing_county)
            edit_mode = True
        else:
            editing_county = None
            form = CountyForm()
            edit_mode = False


    states = State.objects.annotate(
        counties_count=Count("counties", distinct=True),
        total_votes_sum=Sum("counties__results__total_votes"),
        current_votes_sum=Sum("counties__results__current_votes"),
        avg_percent=Avg("counties__results__percent"),
    ).order_by("name")[:TABLE_LIMIT]

    counties = County.objects.select_related("state").order_by("state__name", "name")[:TABLE_LIMIT]

    results = CountyResult.objects.select_related("county", "county__state") \
        .order_by("county__state__name", "county__name")[:TABLE_LIMIT]

    overall = CountyResult.objects.aggregate(
        total_votes_all=Sum("total_votes"),
        current_votes_all=Sum("current_votes"),
        avg_percent_all=Avg("percent"),
        rows_count=Count("id"),
    )

    return render(request, "index.html", {
        "form": form,
        "edit_mode": edit_mode,
        "editing_county": editing_county,
        "states": states,
        "counties": counties,
        "results": results,
        "overall": overall,
        "table_limit": TABLE_LIMIT,
    })
