from pyspark.sql.functions import expr

# Define end-of-quarter dates
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

# Assume df has columns: ID (string), Tags (array<string>), Dates (array<date>)
# For each end-of-quarter date, add a column: required_by_<date>
for date_str in end_of_quarters:
    column_name = f"required_by_{date_str}"
    df = df.withColumn(
        column_name,
        expr(f"aggregate(Dates, true, (acc, x) -> acc and x <= date('{date_str}'))")
    )

# Show the results
df.show(truncate=False)
