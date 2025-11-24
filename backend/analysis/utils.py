import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXCEL_PATH = os.path.join(BASE_DIR, 'data', 'real_estate.xlsx')


def load_data():
    """
    Excel file load karta hai.
    """
    if not os.path.exists(EXCEL_PATH):
        raise FileNotFoundError(f"Excel file not found at {EXCEL_PATH}")

    df = pd.read_excel(EXCEL_PATH)

    print("ORIGINAL COLUMNS:", list(df.columns))

    cols_lower = {c.lower(): c for c in df.columns}

    area_col = None
    for key in cols_lower:
        if "final location" in key or "small location" in key:
            area_col = cols_lower[key]
            break

    year_col = None
    for key in cols_lower:
        if key.strip() == "year":
            year_col = cols_lower[key]
            break

    price_source = None
    for key in cols_lower:
        normalized = key.replace(" ", "_")  
        if "total_sales" in normalized:
            price_source = cols_lower[key]
            break

    demand_source = None
    for key in cols_lower:
        normalized = key.replace(" ", "_")
        if "total_sold" in normalized:
            demand_source = cols_lower[key]
            break



    print("DETECTED area_col =", area_col)
    print("DETECTED year_col =", year_col)
    print("DETECTED price_source =", price_source)
    print("DETECTED demand_source =", demand_source)

    if not area_col or not year_col:
        return df.iloc[0:0]

    df["area"] = df[area_col]

    if price_source:
        df["price"] = df[price_source]
    if demand_source:
        df["demand"] = df[demand_source]

    print("AFTER ADDING:", list(df.columns))

    df.columns = [c.strip().lower() for c in df.columns]
    return df


def filter_by_area(df, areas):
    """
    Given list of areas, unka data filter karo.
    """
    if "area" not in df.columns:
        return df.iloc[0:0]

    clean_areas = [a.lower().strip() for a in areas]
    return df[df["area"].str.lower().isin(clean_areas)]


def build_chart_data(filtered_df, metric="price"):
    """
    Chart ke liye yearly aggregated data.
    Output: [{year: 2021, area: 'Wakad', value: 4500}, ...]
    """
    if metric not in filtered_df.columns:
        return []

    grouped = (
        filtered_df
        .groupby(["year", "area"])[metric]
        .mean()
        .reset_index()
    )

    chart_data = []
    for _, row in grouped.iterrows():
        chart_data.append({
            "year": int(row["year"]),
            "area": str(row["area"]),
            "value": float(row[metric]),
        })
    return chart_data


def build_mock_summary(filtered_df, areas, metric="price"):
    """
    Simple text summary (mock LLM).
    """
    if filtered_df.empty:
        return f"Koi data nahi mila in areas: {', '.join(areas)}."

    areas_str = ", ".join(areas)
    min_year = int(filtered_df["year"].min()) if "year" in filtered_df.columns else None
    max_year = int(filtered_df["year"].max()) if "year" in filtered_df.columns else None

    if metric in filtered_df.columns:
        avg_val = round(filtered_df[metric].mean(), 2)
    else:
        avg_val = None

    summary_parts = [
        f"Data found for {areas_str}."
    ]

    summary_parts.append(f"Year range is approximately {min_year} to {max_year}.")

    if avg_val is not None:
        if metric == "price":
            summary_parts.append(f"Average price is approximately {avg_val}.")
        else:
            summary_parts.append(f"Average demand is approximately {avg_val}.")

    summary_parts.append("Detailed trend chart and table are displayed below.")

    return " ".join(summary_parts)


def build_table_data(filtered_df, metric="price"):
    """
    Table ke data ko list-of-dicts mein convert karna.
    metric ke hisaab se sirf relevant column bhejte hain.
    """
    if metric == "demand" and "demand" in filtered_df.columns:
        cols = ["year", "area", "demand"]
    else:
        # default price
        cols = ["year", "area", "price"]

    available_cols = [c for c in cols if c in filtered_df.columns]
    if not available_cols:
        return []

    table_df = filtered_df[available_cols].sort_values(by="year")
    return table_df.to_dict(orient="records")




