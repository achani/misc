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



from pyspark.sql.functions import col, lit, when, struct, array, explode

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

# Create array of structs: [{date, total_size_if_required_by_false}, ...]
exploded_array = array(*[
    struct(
        lit(date_str).alias("date"),
        when(
            col(f"required_by_{date_str.replace('-', '_')}") == False,
            col("size")
        ).otherwise(lit(0)).alias("size_to_sum")
    )
    for date_str in end_of_quarters
])

# Add array column and explode it
df_with_array = df.withColumn("exploded_structs", exploded_array)
df_exploded = df_with_array.select(explode("exploded_structs").alias("row"))

# Select and group by date
df_final = df_exploded.selectExpr("cast(row.date as date) as date", "row.size_to_sum as size") \
                      .groupBy("date") \
                      .sum("size") \
                      .withColumnRenamed("sum(size)", "total_size") \
                      .orderBy("date")

df_final.show()
