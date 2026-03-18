
Test connections with AWS CLI 
```
aws sts get-caller-identity
```
It returned:
```
{
    "UserId": "AIDA3LJYOQDUBUDNYLKBM",
    "Account": "780191826152",
    "Arn": "arn:aws:iam::780191826152:user/student-s3-london-transport-app"
}
```
and AWS region is **us-east-1**
and S3 bucket is **tetianaomelchenko-london-transport-data**


## how all 10 raw files were used
They were used to build 8 final reports, that contain detailed and summarized data.

## which processed outputs were created
For each raw file the cleaned processed file have been created. 

## which curated reports were created
The business_reports:
- disruptions_by_line
- fares_report
- schedule_coverage
summaries:
- borough_passengers
- line_delay
- top_stations
final_outputs:
- line_operations_report
- transport_report
- 
## what felt different from Day 2
The raw and cleaned data and final reports have been stored in S3

## why Day 3 feels more like real cloud data engineering
Because it's common to use clouds to store date.





