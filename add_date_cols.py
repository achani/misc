from pyspark.sql.functions import expr

# List of end-of-quarter dates
end_of_quarters = [
    '2025-03-31',
    '2025-06-30',
    '2025-09-30',
    '2025-12-31',
    '2026-03-31',
    '2026-06-30',
    '2026-09-30',
    '2026-12-31'
]

# Iterate and add a column for each date
for date_str in end_of_quarters:
    col_name = f"required_by_{date_str.replace('-', '_')}"  # Replace - with _ to make column name safe
    condition_expr = f"""
        CASE
            WHEN Dates IS NULL OR size(Dates) = 0 THEN false
            ELSE aggregate(Dates, true, (acc, x) -> acc AND x <= date('{date_str}'))
        END
    """
    df = df.withColumn(col_name, expr(condition_expr))

