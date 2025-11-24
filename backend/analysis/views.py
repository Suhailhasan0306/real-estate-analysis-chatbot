from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .utils import (
    load_data,
    filter_by_area,
    build_chart_data,
    build_mock_summary,
    build_table_data,
)


@api_view(["POST"])
def analyze_query(request):
    """
    Expect body:
    {
      "query": "Analyze Wakad",
      "metric": "price" | "demand"
    }
    OR
    {
      "areas": ["Wakad", "Akurdi"],
      "metric": "price"
    }
    """
    query = request.data.get("query", "") or ""
    areas = request.data.get("areas")
    metric = request.data.get("metric", "price") 

    if metric not in ["price", "demand"]:
        metric = "price"

    print("BACKEND request.data =", request.data)
    print("BACKEND metric used =", metric)

    if not areas:
        areas = extract_areas_from_query(query)

    if not areas:
        return Response(
            {
                "error": "Areas detect nahi ho payi. Please 'areas' field ya proper query bhejo."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        df = load_data()
    except Exception as e:
        return Response(
            {"error": f"Failed to load Excel data: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    filtered_df = filter_by_area(df, areas)

    chart_data = build_chart_data(filtered_df, metric=metric)
    table_data = build_table_data(filtered_df, metric=metric)
    summary = build_mock_summary(filtered_df, areas, metric=metric)

    response_data = {
        "summary": summary,
        "chartData": chart_data,
        "tableData": table_data,
        "areas": areas,
        "metric": metric,
    }
    return Response(response_data, status=status.HTTP_200_OK)
def extract_areas_from_query(query: str):
    """
    Simple heuristic parsing: query se areas nikalne ki koshish.
    """
    if not query:
        return []

    q = query.lower()

    if "compare" in q and "and" in q:
        mid = (
            q.replace("compare", "")
             .replace("demand trends", "")
             .replace("price trends", "")
        )
        parts = mid.split("and")
        areas = [p.strip().title() for p in parts if p.strip()]
        return areas

    if "analyze" in q:
        words = q.replace("analyze", "").strip().split()
        if words:
            return [" ".join(words).title()]

    if " for " in q:
        after_for = q.split(" for ", 1)[1]

        stop_tokens = [" over ", " in ", " during "]
        stop_index = len(after_for)

        for token in stop_tokens:
            if token in after_for:
                idx = after_for.index(token)
                if idx < stop_index:
                    stop_index = idx

        area_part = after_for[:stop_index].strip()
        if area_part:
            return [area_part.title()]

    words = q.split()
    if words:
        return [words[-1].title()]

    return []
