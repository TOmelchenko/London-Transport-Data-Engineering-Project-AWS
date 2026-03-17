# Day 3 Spark Data Engineering Tasks  
## London Transport Data Engineering Project

Welcome to the **Spark Data Engineering** part of Day 3.

In this file, you will build the **cloud data lake Spark pipeline** for the London Transport project.

On the earlier days, you already solved the same business problem in different ways:

- **Day 1** → local ETL and ELT with PostgreSQL
- **Day 2** → Spark processing with local raw files

On **Day 3**, you will now solve the project in a more realistic cloud-style workflow:

- **S3** stores the full raw data environment
- **Spark** reads data from cloud storage
- **Spark** cleans and processes all datasets
- **Spark** writes processed and curated outputs back to S3

This is an important upgrade.

You are no longer working only with a few local files.  
You are now engineering the **full transport raw data lake**.

This file is fully guided on purpose.

You are not expected to invent the Spark solution by yourself.  
You are expected to follow each step carefully, run the code, observe the result, and learn from the workflow.

---

# 1. Day 3 Spark objective

Your goal in this part is to build a working Spark cloud pipeline that:

- reads the London transport raw files from **S3**
- creates Spark DataFrames for **all source datasets**
- inspects schemas
- cleans and standardizes important fields
- builds processed datasets for each source
- creates joined business-ready reporting datasets
- writes processed and curated outputs back to **S3**

By the end of this file, you should have a working Day 3 cloud data engineering pipeline.

---

# 2. Important note before starting

This time, you are **not** focusing on only three or four files.

For Day 3, all the raw files are in scope:

- `stations.csv`
- `lines.csv`
- `journeys.json`
- `vehicle_types.csv`
- `operators.csv`
- `zones.csv`
- `disruptions.json`
- `fares.csv`
- `boroughs.csv`
- `schedules.xml`

That is the main upgrade of Day 3.

You are now treating the London Transport project like a full raw data environment.

---

# 3. What are we building today?

Today, your Spark pipeline should produce:

## Processed outputs for all source datasets
That means cleaned versions of:
- stations
- lines
- journeys
- vehicle types
- operators
- zones
- disruptions
- fares
- boroughs
- schedules

## Joined reporting outputs
That means business-ready views such as:
- transport activity report
- top stations by passenger count
- average delay by line
- passenger activity by borough
- disruptions by line
- fares by zone and transport mode
- schedule coverage by line

This makes the Day 3 stage much richer and more realistic.

---

# 4. Day 3 Spark flow

Here is the Spark flow you are building:

```text
S3 raw files → Spark DataFrames → Cleaning and standardization → Processed datasets → Joined outputs → Curated reports → Write back to S3
````

More specifically:

```text
raw/stations/stations.csv
raw/lines/lines.csv
raw/journeys/journeys.json
raw/vehicle_types/vehicle_types.csv
raw/operators/operators.csv
raw/zones/zones.csv
raw/disruptions/disruptions.json
raw/fares/fares.csv
raw/boroughs/boroughs.csv
raw/schedules/schedules.xml
        ↓
Spark DataFrames
        ↓
Cleaned and processed datasets
        ↓
Joined business reports
        ↓
processed/...
curated/...
```

That is your Day 3 cloud data engineering workflow.

---

# 5. Step 1 - Create the Day 3 Spark pipeline file

## Your task

Open or create:

```text
src/cloud_pipeline.py
```

This file will contain the full guided cloud Spark pipeline for Day 3.

---

# 6. Step 2 - Start with the imports

## Your task

At the top of `src/cloud_pipeline.py`, add:

```python
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    trim,
    initcap,
    when,
    sum as spark_sum,
    avg,
    count,
    lit
)
```

## Why this matters

These imports prepare the main Spark tools you need:

* `SparkSession` to start Spark
* `col` for column operations
* `trim` for removing extra spaces
* `initcap` for cleaning text capitalization
* aggregation functions such as `sum`, `avg`, and `count`
* `lit` for adding constant values if needed later

This is the beginning of your Day 3 Spark workflow.

---

# 7. Step 3 - Define project paths and bucket information

## Your task

Still in `src/cloud_pipeline.py`, add:

```python
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FOLDER = PROJECT_ROOT / "data" / "output"

BUCKET_NAME = "london-transport-day3-yourname-2026"

RAW_BASE = f"s3a://{BUCKET_NAME}/raw"
PROCESSED_BASE = f"s3a://{BUCKET_NAME}/processed"
CURATED_BASE = f"s3a://{BUCKET_NAME}/curated"
```

## Important note

Replace:

```text
london-transport-day3-yourname-2026
```

with **your real bucket name**.

## Why this matters

Spark needs to know where the S3 files live.

This makes your script clearly connected to your cloud data lake layout.

---

# 8. Step 4 - Start the Spark session

## Your task

Add this function:

```python
def create_spark_session():
    spark = (
        SparkSession.builder
        .appName("LondonTransportCloudDataLakeProject")
        .getOrCreate()
    )
    return spark
```

## Why this matters

This starts Spark and gives your project a clear application name.

That is the standard first step in a Spark project.

---

# 9. Step 5 - Read all raw files from S3

## Your task

Add this function:

```python
def load_dataframes(spark):
    stations_df = spark.read.option("header", True).csv(f"{RAW_BASE}/stations/stations.csv")
    lines_df = spark.read.option("header", True).csv(f"{RAW_BASE}/lines/lines.csv")
    journeys_df = spark.read.option("multiline", True).json(f"{RAW_BASE}/journeys/journeys.json")
    vehicle_types_df = spark.read.option("header", True).csv(f"{RAW_BASE}/vehicle_types/vehicle_types.csv")
    operators_df = spark.read.option("header", True).csv(f"{RAW_BASE}/operators/operators.csv")
    zones_df = spark.read.option("header", True).csv(f"{RAW_BASE}/zones/zones.csv")
    disruptions_df = spark.read.option("multiline", True).json(f"{RAW_BASE}/disruptions/disruptions.json")
    fares_df = spark.read.option("header", True).csv(f"{RAW_BASE}/fares/fares.csv")
    boroughs_df = spark.read.option("header", True).csv(f"{RAW_BASE}/boroughs/boroughs.csv")
    schedules_df = (
        spark.read
        .format("xml")
        .option("rowTag", "schedule")
        .load(f"{RAW_BASE}/schedules/schedules.xml")
    )

    return (
        stations_df,
        lines_df,
        journeys_df,
        vehicle_types_df,
        operators_df,
        zones_df,
        disruptions_df,
        fares_df,
        boroughs_df,
        schedules_df
    )
```

## Important note

The XML reader above uses Spark XML format support.
If your environment does not support `.format("xml")`, ask your instructor first before trying random fixes.

For this guided project, use the provided environment expectations.

## Why this matters

This step reads the **full raw environment** from S3, not from local folders.

That is one of the biggest Day 3 upgrades.

---

# 10. Step 6 - Inspect schemas for all datasets

## Your task

Add this function:

```python
def inspect_dataframes(
    stations_df,
    lines_df,
    journeys_df,
    vehicle_types_df,
    operators_df,
    zones_df,
    disruptions_df,
    fares_df,
    boroughs_df,
    schedules_df
):
    print("\n=== Stations Schema ===")
    stations_df.printSchema()

    print("\n=== Lines Schema ===")
    lines_df.printSchema()

    print("\n=== Journeys Schema ===")
    journeys_df.printSchema()

    print("\n=== Vehicle Types Schema ===")
    vehicle_types_df.printSchema()

    print("\n=== Operators Schema ===")
    operators_df.printSchema()

    print("\n=== Zones Schema ===")
    zones_df.printSchema()

    print("\n=== Disruptions Schema ===")
    disruptions_df.printSchema()

    print("\n=== Fares Schema ===")
    fares_df.printSchema()

    print("\n=== Boroughs Schema ===")
    boroughs_df.printSchema()

    print("\n=== Schedules Schema ===")
    schedules_df.printSchema()
```

## Why this matters

Checking schemas is one of the most important Spark habits.

It helps you understand:

* column names
* data types
* whether Spark read the files correctly

A data engineer should never transform data blindly.

---

# 11. Step 7 - Preview some sample rows

## Your task

Add this function:

```python
def preview_data(
    stations_df,
    lines_df,
    journeys_df,
    vehicle_types_df,
    operators_df,
    zones_df,
    disruptions_df,
    fares_df,
    boroughs_df,
    schedules_df
):
    print("\n=== Stations Preview ===")
    stations_df.show(3, truncate=False)

    print("\n=== Lines Preview ===")
    lines_df.show(3, truncate=False)

    print("\n=== Journeys Preview ===")
    journeys_df.show(3, truncate=False)

    print("\n=== Vehicle Types Preview ===")
    vehicle_types_df.show(3, truncate=False)

    print("\n=== Operators Preview ===")
    operators_df.show(3, truncate=False)

    print("\n=== Zones Preview ===")
    zones_df.show(3, truncate=False)

    print("\n=== Disruptions Preview ===")
    disruptions_df.show(3, truncate=False)

    print("\n=== Fares Preview ===")
    fares_df.show(3, truncate=False)

    print("\n=== Boroughs Preview ===")
    boroughs_df.show(3, truncate=False)

    print("\n=== Schedules Preview ===")
    schedules_df.show(3, truncate=False)
```

## Why this matters

This helps you notice:

* extra spaces
* inconsistent capitalization
* missing values
* unusual records

That is part of real data engineering work.

---

# 12. Step 8 - Create text-cleaning helpers

## Your task

Add these helper functions:

```python
def normalize_text_column(df, column_name):
    return df.withColumn(column_name, initcap(trim(col(column_name))))


def trim_column(df, column_name):
    return df.withColumn(column_name, trim(col(column_name)))
```

## Why this matters

Many raw datasets contain:

* extra spaces
* inconsistent capitalization

Reusable helpers make your pipeline cleaner and easier to maintain.

---

# 13. Step 9 - Clean the stations DataFrame

## Your task

Add this function:

```python
def clean_stations_df(stations_df):
    cleaned_df = (
        stations_df
        .filter(col("station_id").isNotNull() & (trim(col("station_id")) != ""))
        .dropDuplicates(["station_id"])
        .withColumn("station_id", trim(col("station_id")))
        .withColumn("station_name", initcap(trim(col("station_name"))))
        .withColumn("borough_id", trim(col("borough_id")))
        .withColumn("zone_id", trim(col("zone_id")))
        .withColumn("line_id", trim(col("line_id")))
        .withColumn("station_type", initcap(trim(col("station_type"))))
    )
    return cleaned_df
```

## Why this matters

Stations are core reference data, so they must be cleaned before use.

---

# 14. Step 10 - Clean the lines DataFrame

## Your task

Add this function:

```python
def clean_lines_df(lines_df):
    cleaned_df = (
        lines_df
        .filter(col("line_id").isNotNull() & (trim(col("line_id")) != ""))
        .dropDuplicates(["line_id"])
        .withColumn("line_id", trim(col("line_id")))
        .withColumn("line_name", initcap(trim(col("line_name"))))
        .withColumn("transport_mode", initcap(trim(col("transport_mode"))))
        .withColumn("operator_id", trim(col("operator_id")))
        .withColumn("vehicle_type_id", trim(col("vehicle_type_id")))
        .withColumn("service_status", initcap(trim(col("service_status"))))
        .withColumn("snapshot_date", trim(col("snapshot_date")))
    )
    return cleaned_df
```

---

# 15. Step 11 - Clean the journeys DataFrame

## Your task

Add this function:

```python
def clean_journeys_df(journeys_df):
    cleaned_df = (
        journeys_df
        .filter(col("journey_id").isNotNull() & (trim(col("journey_id")) != ""))
        .filter(col("station_id").isNotNull() & (trim(col("station_id")) != ""))
        .filter(col("line_id").isNotNull() & (trim(col("line_id")) != ""))
        .filter(trim(col("passenger_count")).rlike("^[0-9]+$"))
        .filter(trim(col("delay_minutes")).rlike("^[0-9]+$"))
        .filter(trim(col("journey_date")).rlike("^[0-9]{4}-[0-9]{2}-[0-9]{2}$"))
        .withColumn("journey_id", trim(col("journey_id")))
        .withColumn("station_id", trim(col("station_id")))
        .withColumn("line_id", trim(col("line_id")))
        .withColumn("passenger_count", trim(col("passenger_count")).cast("int"))
        .withColumn("delay_minutes", trim(col("delay_minutes")).cast("int"))
        .withColumn("journey_date", trim(col("journey_date")).cast("date"))
        .withColumn("time_band", initcap(trim(col("time_band"))))
        .withColumn("entry_exit_flag", initcap(trim(col("entry_exit_flag"))))
    )
    return cleaned_df
```

## Why this matters

Journeys are the main event-level dataset.

This is where the transport activity lives.

---

# 16. Step 12 - Clean the vehicle types DataFrame

## Your task

Add this function:

```python
def clean_vehicle_types_df(vehicle_types_df):
    cleaned_df = (
        vehicle_types_df
        .filter(col("vehicle_type_id").isNotNull() & (trim(col("vehicle_type_id")) != ""))
        .dropDuplicates(["vehicle_type_id"])
        .withColumn("vehicle_type_id", trim(col("vehicle_type_id")))
        .withColumn("mode_name", initcap(trim(col("mode_name"))))
        .withColumn("capacity_range", trim(col("capacity_range")))
        .withColumn("accessibility_flag", initcap(trim(col("accessibility_flag"))))
        .withColumn("energy_type", initcap(trim(col("energy_type"))))
        .withColumn("report_date", trim(col("report_date")))
    )
    return cleaned_df
```

---

# 17. Step 13 - Clean the operators DataFrame

## Your task

Add this function:

```python
def clean_operators_df(operators_df):
    cleaned_df = (
        operators_df
        .filter(col("operator_id").isNotNull() & (trim(col("operator_id")) != ""))
        .dropDuplicates(["operator_id"])
        .withColumn("operator_id", trim(col("operator_id")))
        .withColumn("operator_name", initcap(trim(col("operator_name"))))
        .withColumn("service_type", initcap(trim(col("service_type"))))
        .withColumn("contract_region", initcap(trim(col("contract_region"))))
        .withColumn("status_flag", initcap(trim(col("status_flag"))))
        .withColumn("report_date", trim(col("report_date")))
    )
    return cleaned_df
```

---

# 18. Step 14 - Clean the zones DataFrame

## Your task

Add this function:

```python
def clean_zones_df(zones_df):
    cleaned_df = (
        zones_df
        .filter(col("zone_id").isNotNull() & (trim(col("zone_id")) != ""))
        .dropDuplicates(["zone_id"])
        .withColumn("zone_id", trim(col("zone_id")))
        .withColumn("zone_name", initcap(trim(col("zone_name"))))
        .withColumn("fare_group", initcap(trim(col("fare_group"))))
        .withColumn("peak_multiplier", trim(col("peak_multiplier")))
        .withColumn("status_note", initcap(trim(col("status_note"))))
        .withColumn("report_date", trim(col("report_date")))
    )
    return cleaned_df
```

---

# 19. Step 15 - Clean the disruptions DataFrame

## Your task

Add this function:

```python
def clean_disruptions_df(disruptions_df):
    cleaned_df = (
        disruptions_df
        .filter(col("disruption_id").isNotNull() & (trim(col("disruption_id")) != ""))
        .filter(col("line_id").isNotNull() & (trim(col("line_id")) != ""))
        .withColumn("disruption_id", trim(col("disruption_id")))
        .withColumn("line_id", trim(col("line_id")))
        .withColumn("disruption_type", initcap(trim(col("disruption_type"))))
        .withColumn("severity", initcap(trim(col("severity"))))
        .withColumn("affected_station_id", trim(col("affected_station_id")))
        .withColumn("disruption_date", trim(col("disruption_date")))
        .filter(trim(col("estimated_delay_minutes")).rlike("^[0-9]+$"))
        .withColumn("estimated_delay_minutes", trim(col("estimated_delay_minutes")).cast("int"))
    )
    return cleaned_df
```

---

# 20. Step 16 - Clean the fares DataFrame

## Your task

Add this function:

```python
def clean_fares_df(fares_df):
    cleaned_df = (
        fares_df
        .filter(col("fare_id").isNotNull() & (trim(col("fare_id")) != ""))
        .filter(col("zone_id").isNotNull() & (trim(col("zone_id")) != ""))
        .dropDuplicates(["fare_id"])
        .withColumn("fare_id", trim(col("fare_id")))
        .withColumn("zone_id", trim(col("zone_id")))
        .withColumn("transport_mode", initcap(trim(col("transport_mode"))))
        .filter(trim(col("base_fare")).rlike("^[0-9]+(\\.[0-9]+)?$"))
        .filter(trim(col("peak_fare")).rlike("^[0-9]+(\\.[0-9]+)?$"))
        .withColumn("base_fare", trim(col("base_fare")).cast("double"))
        .withColumn("peak_fare", trim(col("peak_fare")).cast("double"))
        .withColumn("effective_date", trim(col("effective_date")))
    )
    return cleaned_df
```

---

# 21. Step 17 - Clean the boroughs DataFrame

## Your task

Add this function:

```python
def clean_boroughs_df(boroughs_df):
    cleaned_df = (
        boroughs_df
        .filter(col("borough_id").isNotNull() & (trim(col("borough_id")) != ""))
        .dropDuplicates(["borough_id"])
        .withColumn("borough_id", trim(col("borough_id")))
        .withColumn("borough_name", initcap(trim(col("borough_name"))))
        .withColumn("region_group", initcap(trim(col("region_group"))))
        .withColumn("population_band", initcap(trim(col("population_band"))))
        .withColumn("avg_daily_ridership_band", initcap(trim(col("avg_daily_ridership_band"))))
        .withColumn("report_month", trim(col("report_month")))
    )
    return cleaned_df
```

---

# 22. Step 18 - Clean the schedules DataFrame

## Your task

Add this function:

```python
def clean_schedules_df(schedules_df):
    cleaned_df = (
        schedules_df
        .filter(col("schedule_id").isNotNull() & (trim(col("schedule_id")) != ""))
        .withColumn("schedule_id", trim(col("schedule_id")))
        .withColumn("station_id", trim(col("station_id")))
        .withColumn("line_id", trim(col("line_id")))
        .withColumn("planned_start_time", trim(col("planned_start_time")))
        .withColumn("planned_end_time", trim(col("planned_end_time")))
        .withColumn("service_day", initcap(trim(col("service_day"))))
        .withColumn("status_note", initcap(trim(col("status_note"))))
    )
    return cleaned_df
```

---

# 23. Step 19 - Build the main transport activity report

## Your task

Add this function:

```python
def build_transport_report_df(stations_df, lines_df, journeys_df, boroughs_df, zones_df):
    report_df = (
        journeys_df.alias("j")
        .join(stations_df.alias("s"), col("j.station_id") == col("s.station_id"), "inner")
        .join(lines_df.alias("l"), col("j.line_id") == col("l.line_id"), "inner")
        .join(boroughs_df.alias("b"), col("s.borough_id") == col("b.borough_id"), "left")
        .join(zones_df.alias("z"), col("s.zone_id") == col("z.zone_id"), "left")
        .select(
            col("j.journey_id"),
            col("j.journey_date"),
            col("s.station_id"),
            col("s.station_name"),
            col("s.borough_id"),
            col("b.borough_name"),
            col("s.zone_id"),
            col("z.zone_name"),
            col("l.line_id"),
            col("l.line_name"),
            col("l.transport_mode"),
            col("j.passenger_count"),
            col("j.delay_minutes"),
            col("j.time_band"),
            col("j.entry_exit_flag")
        )
    )
    return report_df
```

## Why this matters

This is the main joined business report for transport activity.

---

# 24. Step 20 - Build an operator and vehicle enrichment report

## Your task

Add this function:

```python
def build_line_operations_report_df(lines_df, operators_df, vehicle_types_df):
    report_df = (
        lines_df.alias("l")
        .join(operators_df.alias("o"), col("l.operator_id") == col("o.operator_id"), "left")
        .join(vehicle_types_df.alias("v"), col("l.vehicle_type_id") == col("v.vehicle_type_id"), "left")
        .select(
            col("l.line_id"),
            col("l.line_name"),
            col("l.transport_mode"),
            col("o.operator_name"),
            col("o.service_type"),
            col("v.mode_name"),
            col("v.capacity_range"),
            col("v.energy_type")
        )
    )
    return report_df
```

---

# 25. Step 21 - Build a disruptions report

## Your task

Add this function:

```python
def build_disruptions_by_line_df(disruptions_df, lines_df):
    return (
        disruptions_df.alias("d")
        .join(lines_df.alias("l"), col("d.line_id") == col("l.line_id"), "inner")
        .groupBy("l.line_name")
        .agg(
            count("d.disruption_id").alias("total_disruptions"),
            avg("d.estimated_delay_minutes").alias("avg_estimated_delay")
        )
        .orderBy(col("total_disruptions").desc())
    )
```

---

# 26. Step 22 - Build a fares report

## Your task

Add this function:

```python
def build_fares_report_df(fares_df, zones_df):
    return (
        fares_df.alias("f")
        .join(zones_df.alias("z"), col("f.zone_id") == col("z.zone_id"), "left")
        .select(
            col("f.fare_id"),
            col("f.zone_id"),
            col("z.zone_name"),
            col("f.transport_mode"),
            col("f.base_fare"),
            col("f.peak_fare"),
            col("f.effective_date")
        )
    )
```

---

# 27. Step 23 - Build a schedules report

## Your task

Add this function:

```python
def build_schedule_coverage_df(schedules_df, lines_df):
    return (
        schedules_df.alias("s")
        .join(lines_df.alias("l"), col("s.line_id") == col("l.line_id"), "left")
        .groupBy("l.line_name", "s.service_day")
        .agg(count("s.schedule_id").alias("total_schedules"))
        .orderBy(col("total_schedules").desc())
    )
```

---

# 28. Step 24 - Build simple summary reports

## Your task

Add these functions:

### Top stations by passengers

```python
def build_top_stations_df(transport_report_df):
    return (
        transport_report_df
        .groupBy("station_name")
        .agg(spark_sum("passenger_count").alias("total_passengers"))
        .orderBy(col("total_passengers").desc())
    )
```

### Average delay by line

```python
def build_line_delay_df(transport_report_df):
    return (
        transport_report_df
        .groupBy("line_name")
        .agg(avg("delay_minutes").alias("avg_delay_minutes"))
        .orderBy(col("avg_delay_minutes").desc())
    )
```

### Passenger activity by borough

```python
def build_borough_passengers_df(transport_report_df):
    return (
        transport_report_df
        .groupBy("borough_name")
        .agg(spark_sum("passenger_count").alias("total_passengers"))
        .orderBy(col("total_passengers").desc())
    )
```

---

# 29. Step 25 - Write processed datasets to S3

## Your task

Add this function:

```python
def write_processed_outputs(
    stations_df,
    lines_df,
    journeys_df,
    vehicle_types_df,
    operators_df,
    zones_df,
    disruptions_df,
    fares_df,
    boroughs_df,
    schedules_df
):
    stations_df.write.mode("overwrite").option("header", True).csv(f"{PROCESSED_BASE}/stations/")
    lines_df.write.mode("overwrite").option("header", True).csv(f"{PROCESSED_BASE}/lines/")
    journeys_df.write.mode("overwrite").option("header", True).csv(f"{PROCESSED_BASE}/journeys/")
    vehicle_types_df.write.mode("overwrite").option("header", True).csv(f"{PROCESSED_BASE}/vehicle_types/")
    operators_df.write.mode("overwrite").option("header", True).csv(f"{PROCESSED_BASE}/operators/")
    zones_df.write.mode("overwrite").option("header", True).csv(f"{PROCESSED_BASE}/zones/")
    disruptions_df.write.mode("overwrite").option("header", True).csv(f"{PROCESSED_BASE}/disruptions/")
    fares_df.write.mode("overwrite").option("header", True).csv(f"{PROCESSED_BASE}/fares/")
    boroughs_df.write.mode("overwrite").option("header", True).csv(f"{PROCESSED_BASE}/boroughs/")
    schedules_df.write.mode("overwrite").option("header", True).csv(f"{PROCESSED_BASE}/schedules/")
```

## Why this matters

This gives each raw dataset a cleaned and processed version in the cloud.

That is very important for Day 3.

---

# 30. Step 26 - Write curated outputs to S3

## Your task

Add this function:

```python
def write_curated_outputs(
    transport_report_df,
    line_operations_report_df,
    disruptions_by_line_df,
    fares_report_df,
    schedule_coverage_df,
    top_stations_df,
    line_delay_df,
    borough_passengers_df
):
    transport_report_df.write.mode("overwrite").option("header", True).csv(f"{CURATED_BASE}/final_outputs/transport_report/")
    line_operations_report_df.write.mode("overwrite").option("header", True).csv(f"{CURATED_BASE}/final_outputs/line_operations_report/")
    disruptions_by_line_df.write.mode("overwrite").option("header", True).csv(f"{CURATED_BASE}/business_reports/disruptions_by_line/")
    fares_report_df.write.mode("overwrite").option("header", True).csv(f"{CURATED_BASE}/business_reports/fares_report/")
    schedule_coverage_df.write.mode("overwrite").option("header", True).csv(f"{CURATED_BASE}/business_reports/schedule_coverage/")
    top_stations_df.write.mode("overwrite").option("header", True).csv(f"{CURATED_BASE}/summaries/top_stations/")
    line_delay_df.write.mode("overwrite").option("header", True).csv(f"{CURATED_BASE}/summaries/line_delay/")
    borough_passengers_df.write.mode("overwrite").option("header", True).csv(f"{CURATED_BASE}/summaries/borough_passengers/")
```

---

# 31. Step 27 - Create the full main pipeline function

## Your task

Add this full `main()` function:

```python
def main():
    spark = create_spark_session()

    (
        stations_df,
        lines_df,
        journeys_df,
        vehicle_types_df,
        operators_df,
        zones_df,
        disruptions_df,
        fares_df,
        boroughs_df,
        schedules_df
    ) = load_dataframes(spark)

    inspect_dataframes(
        stations_df,
        lines_df,
        journeys_df,
        vehicle_types_df,
        operators_df,
        zones_df,
        disruptions_df,
        fares_df,
        boroughs_df,
        schedules_df
    )

    preview_data(
        stations_df,
        lines_df,
        journeys_df,
        vehicle_types_df,
        operators_df,
        zones_df,
        disruptions_df,
        fares_df,
        boroughs_df,
        schedules_df
    )

    stations_clean_df = clean_stations_df(stations_df)
    lines_clean_df = clean_lines_df(lines_df)
    journeys_clean_df = clean_journeys_df(journeys_df)
    vehicle_types_clean_df = clean_vehicle_types_df(vehicle_types_df)
    operators_clean_df = clean_operators_df(operators_df)
    zones_clean_df = clean_zones_df(zones_df)
    disruptions_clean_df = clean_disruptions_df(disruptions_df)
    fares_clean_df = clean_fares_df(fares_df)
    boroughs_clean_df = clean_boroughs_df(boroughs_df)
    schedules_clean_df = clean_schedules_df(schedules_df)

    transport_report_df = build_transport_report_df(
        stations_clean_df,
        lines_clean_df,
        journeys_clean_df,
        boroughs_clean_df,
        zones_clean_df
    )

    line_operations_report_df = build_line_operations_report_df(
        lines_clean_df,
        operators_clean_df,
        vehicle_types_clean_df
    )

    disruptions_by_line_df = build_disruptions_by_line_df(
        disruptions_clean_df,
        lines_clean_df
    )

    fares_report_df = build_fares_report_df(
        fares_clean_df,
        zones_clean_df
    )

    schedule_coverage_df = build_schedule_coverage_df(
        schedules_clean_df,
        lines_clean_df
    )

    top_stations_df = build_top_stations_df(transport_report_df)
    line_delay_df = build_line_delay_df(transport_report_df)
    borough_passengers_df = build_borough_passengers_df(transport_report_df)

    print("\n=== Transport Report Preview ===")
    transport_report_df.show(10, truncate=False)

    print("\n=== Line Operations Report Preview ===")
    line_operations_report_df.show(10, truncate=False)

    print("\n=== Disruptions By Line Preview ===")
    disruptions_by_line_df.show(10, truncate=False)

    print("\n=== Fares Report Preview ===")
    fares_report_df.show(10, truncate=False)

    print("\n=== Schedule Coverage Preview ===")
    schedule_coverage_df.show(10, truncate=False)

    write_processed_outputs(
        stations_clean_df,
        lines_clean_df,
        journeys_clean_df,
        vehicle_types_clean_df,
        operators_clean_df,
        zones_clean_df,
        disruptions_clean_df,
        fares_clean_df,
        boroughs_clean_df,
        schedules_clean_df
    )

    write_curated_outputs(
        transport_report_df,
        line_operations_report_df,
        disruptions_by_line_df,
        fares_report_df,
        schedule_coverage_df,
        top_stations_df,
        line_delay_df,
        borough_passengers_df
    )

    print("\nCloud Spark pipeline completed successfully.")
    spark.stop()
```

And add this at the bottom:

```python
if __name__ == "__main__":
    main()
```

---

# 32. Step 28 - Run the cloud Spark pipeline

## Your task

From the project root, run:

```bash
python src/cloud_pipeline.py
```

or if needed:

```bash
python3 src/cloud_pipeline.py
```

## What you should expect

If everything is correct, you should see:

* schemas printed
* preview tables
* success message

Something like:

```text
Cloud Spark pipeline completed successfully.
```

---

# 33. Step 29 - Check S3 outputs

## Your task

After the pipeline finishes, check the processed and curated outputs in S3.

Run:

```bash
aws s3 ls s3://london-transport-day3-yourname-2026/processed/ --recursive
aws s3 ls s3://london-transport-day3-yourname-2026/curated/ --recursive
```

## What should happen

You should see many files written by Spark into:

* `processed/...`
* `curated/...`

That confirms your cloud pipeline worked.

---

# 34. Step 30 - Add project notes

## Your task

Open:

```text
docs/project_notes.md
```

and write short notes about:

* how all 10 raw files were used
* which processed outputs were created
* which curated reports were created
* what felt different from Day 2
* why Day 3 feels more like real cloud data engineering

---

# 35. Step 31 - Commit and push your progress

## Your task

After completing the Day 3 Spark work, push your progress.

Example:

```bash
git add .
git commit -m "Complete Day 3 cloud Spark data engineering pipeline"
git push
```

---

# 36. What makes this stage realistic

This Day 3 stage reflects real data engineering habits such as:

* organizing cloud storage carefully
* using layered data lake design
* reading many source datasets
* cleaning all datasets
* creating processed outputs
* creating curated business-ready outputs
* using Spark against cloud storage instead of only local files

That is why this stage is a real upgrade.

---

# 37. What you should understand after finishing

By the end of this Spark part, you should understand that:

* S3 changes the project from local storage into cloud storage
* all raw datasets can be engineered together in one cloud workflow
* Spark can process cloud data, not only local files
* processed and curated layers are important in real data engineering
* the same business project becomes stronger when its storage architecture becomes more realistic

That is the main learning goal of Day 3.

---

# 38. Final Day 3 reminder

At the end of Day 3, you should now have:

* a public Day 3 GitHub repository
* a working S3 data lake layout
* all raw files in cloud storage
* a working Spark cloud pipeline
* processed outputs in S3
* curated business outputs in S3
* project notes
* checkpoint answers
* multiple commits showing your progress

That is a very strong Day 3 achievement.

---

# 39. Final message

Treat this Day 3 stage like real junior cloud data engineering work.

The goal is not only to make Spark run.

The goal is to understand how a full raw transport data environment can be organized, processed, and transformed in a cloud data lake workflow using **S3 and Spark**.

That is a meaningful and realistic step in becoming a stronger data engineer.

Now continue to the checkpoint file:

* [README 05 - Day 3 Checkpoint Answers](./README_05_Day3_Checkpoint_Answers.md)


