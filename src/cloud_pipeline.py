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
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FOLDER = PROJECT_ROOT / "data" / "output"

BUCKET_NAME = os.environ["BUCKET_NAME"]

RAW_BASE = f"s3a://{BUCKET_NAME}/raw"
PROCESSED_BASE = f"s3a://{BUCKET_NAME}/processed"
CURATED_BASE = f"s3a://{BUCKET_NAME}/curated"

# Start the Spark session
def create_spark_session(app_name="LondonTransportSparkProject"):
    return (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .config("spark.driver.host", "127.0.0.1")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .config(
            "spark.jars.packages",
            "org.apache.hadoop:hadoop-aws:3.4.2,com.amazonaws:aws-java-sdk-bundle:1.12.262",
        )
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config(
            "spark.hadoop.fs.s3a.aws.credentials.provider",
            "com.amazonaws.auth.DefaultAWSCredentialsProviderChain",
    )
    .getOrCreate()
    )

# Read all raw files from S3
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

# Inspect schemas for all datasets
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

# Preview some sample rows  
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

# Create text-cleaning helpers
def normalize_text_column(df, column_name):
    return df.withColumn(column_name, initcap(trim(col(column_name))))


def trim_column(df, column_name):
    return df.withColumn(column_name, trim(col(column_name)))   

# Clean the stations DataFrame
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

# Clean the lines DataFrame
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

# Clean the journeys DataFrame
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

# Clean the vehicle types DataFrame
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

# Clean the operators DataFrame
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

# Clean the zones DataFrame
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

# Clean the disruptions DataFrame
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

# Clean the fares DataFrame
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

# Clean the boroughs DataFrame
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

# Clean the schedules DataFrame
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

# Build the main transport activity report
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

# Build an operator and vehicle enrichment report
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

# Build a disruptions report
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

# Build a fares report
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

# Build a schedules report
def build_schedule_coverage_df(schedules_df, lines_df):
    return (
        schedules_df.alias("s")
        .join(lines_df.alias("l"), col("s.line_id") == col("l.line_id"), "left")
        .groupBy("l.line_name", "s.service_day")
        .agg(count("s.schedule_id").alias("total_schedules"))
        .orderBy(col("total_schedules").desc())
    )

# Build simple summary reports
def build_top_stations_df(transport_report_df):
    return (
        transport_report_df
        .groupBy("station_name")
        .agg(spark_sum("passenger_count").alias("total_passengers"))
        .orderBy(col("total_passengers").desc())
    )

def build_line_delay_df(transport_report_df):
    return (
        transport_report_df
        .groupBy("line_name")
        .agg(avg("delay_minutes").alias("avg_delay_minutes"))
        .orderBy(col("avg_delay_minutes").desc())
    )

def build_borough_passengers_df(transport_report_df):
    return (
        transport_report_df
        .groupBy("borough_name")
        .agg(spark_sum("passenger_count").alias("total_passengers"))
        .orderBy(col("total_passengers").desc())
    )

# Write processed datasets to S3
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

# Write curated outputs to S3
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

if __name__ == "__main__":
    main()    