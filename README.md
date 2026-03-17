# London Transport Data Engineering Project  
## Day 3 – Cloud Data Lake Engineering Stage

Welcome to **Day 3** of the London Transport Data Engineering Project.

This repository contains the **cloud data lake stage** of the project.

This is a **new standalone GitHub repository** for Day 3, but it is part of the same larger full-stack data engineering journey.

On the previous days, you already worked on the same business problem in different ways:

- **Day 1** → local ETL and ELT with PostgreSQL
- **Day 2** → Spark processing with local raw files

On **Day 3**, you will work on the **same London transport business scenario again**, but now in a much more cloud-style data engineering setup:

- **S3** as cloud storage
- **Spark** as the processing engine
- **all raw files** included in the workflow
- **raw, processed, and curated-style layers** in the storage design

This is a major upgrade in the project.

---

# 1. Why this stage matters

Day 3 is important because this is where the project starts to feel much more like a **real cloud data engineering project**.

On Day 1 and Day 2, you already learned how to solve the business problem locally.

That was necessary.

But real data engineering work often does not stay only on a personal laptop with local files.

In real projects, teams often work with:

- cloud storage
- large groups of raw files
- structured storage layers
- processing pipelines that move data between layers
- output zones for downstream analytics

That is exactly the direction of Day 3.

So this stage is not just “upload files to S3.”

This stage is about learning how to think about the project as a **cloud data lake pipeline**.

---

# 2. Business scenario

You are working as a **junior data engineer** for a **London transport analytics team**.

The transport organization receives raw operational data from many internal systems.

Management wants the data engineering team to prepare this data so that analysts and decision-makers can answer questions such as:

- Which stations are the busiest?
- Which lines carry the most passengers?
- Which journeys are delayed most often?
- Which disruption types appear most often?
- Which boroughs and zones show the highest transport activity?
- Which operators and vehicle types are associated with different parts of the network?
- How can the full raw data environment be organized more professionally in the cloud?

That last point is especially important on Day 3.

Today, you are not only answering business questions.  
You are also organizing and engineering the **full raw data environment** in a more realistic cloud architecture.

---

# 3. Your role in this project

In this project, you are acting as a:

## **Junior Data Engineer**

Your job is not only to run code.

Your job is to understand:

- what the business problem is
- what the raw data sources are
- how cloud storage changes the workflow
- how data should be organized in storage layers
- how Spark processes the data from cloud storage
- how to generate meaningful outputs for analytics use

This repository is fully guided on purpose.

You are not expected to invent a complete cloud data engineering solution by yourself.

Instead, you are expected to:

- follow the steps carefully
- understand what each step is doing
- run the provided code
- observe the results
- keep your GitHub repository organized
- learn from the workflow

That is exactly the goal.

---

# 4. What Day 3 is about

Day 3 is about:

## **Cloud Data Lake Engineering with S3 and Spark**

That means you will:

- work with **all raw files**
- place them into **S3**
- organize S3 into meaningful storage layers
- read all the datasets with **Spark**
- clean and process all of them
- generate processed and curated outputs
- write results back to **S3**

This makes the project feel much bigger and more realistic than Day 2.

Day 2 focused mainly on Spark processing.

Day 3 focuses on **Spark + cloud storage architecture + full raw data environment**.

---

# 5. How Day 3 connects to the previous days

This full project is designed as one connected journey.

## Day 1
You built the local foundation using:
- raw files
- PostgreSQL
- ETL
- ELT

## Day 2
You rebuilt the same business logic using:
- Spark
- Spark DataFrames
- Spark joins
- Spark aggregations

## Day 3
You now move the project into a **cloud data lake architecture** using:
- S3
- Spark
- all raw files
- layered cloud storage design

So Day 3 is not a disconnected topic.

It is the next natural step in the same project.

The business scenario stays the same.  
The data engineering environment becomes more realistic and more advanced.

---

# 6. What makes this Day 3 stage a real upgrade

This stage is a real upgrade because:

- you are no longer working with only local files
- you are no longer using only a subset of the raw project environment
- you are now engineering **all the raw data sources**
- you are organizing the storage in cloud layers
- you are reading and writing data in a more cloud-style workflow
- you are making the project look more like a real data engineering platform

So even if some Spark ideas feel familiar from Day 2, the overall project architecture is stronger and more realistic now.

That is the main value of this stage.

---

# 7. The full raw data environment for Day 3

On Day 3, all of the raw project files come back into the story.

That means the project now includes the full raw source environment:

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

This is intentional.

On the earlier days, students mainly focused on the most important core files first.

On Day 3, you now work with the **full raw transport data environment** and treat it like a real cloud data lake engineering problem.

That is one of the biggest conceptual upgrades of the day.

---

# 8. How to think about the cloud data lake on Day 3

For Day 3, you should not think of S3 as “just a bucket with files.”

You should think of S3 as the **cloud storage foundation of the project**.

That means the storage should be organized in a structured way.

A simple example is:

- **raw layer** → original uploaded source files
- **processed layer** → cleaned and transformed outputs
- **curated layer** → more business-ready outputs and summaries

This layered thinking is important because it helps you understand how data engineering projects are usually structured in the cloud.

That is one of the most important ideas of today.

---

# 9. Why Spark is still used today

Yes — Spark is still part of this stage.

That is important.

If Day 3 was only about uploading files to S3, it would be too small and not rich enough as a project stage.

So Day 3 combines:

- **S3** for cloud storage
- **Spark** for processing

That means students will continue to use Spark, but now against the **cloud raw data lake environment** instead of only local files.

This is what makes Day 3 sound and feel like real data engineering.

---

# 10. Environment note for students

For the technical setup in this repository:

- **Windows students** will begin from **Git Bash**
- then enter **WSL**
- and continue the project from there

- **macOS students** will begin from **Terminal**

After those environment-specific startup steps, everyone will continue with the **same Day 3 workflow**.

This is very important because Day 3 includes Spark, and the terminal environment matters.

So please do not worry if the beginning looks slightly different depending on your operating system.  
The main project workflow will still be shared by everyone.

---

# 11. What you are expected to build today

By the end of Day 3, you should have:

- a working Day 3 GitHub repository
- a clear S3 data lake folder structure
- all raw files uploaded and organized in S3
- Spark reading all required source files from S3
- cleaning and transformation logic for all source datasets
- processed and curated outputs written back to S3
- project notes written
- checkpoint answers completed
- your GitHub progress pushed regularly

This is a serious full-day engineering stage.

Please take it seriously.

---

# 12. Why this stage is valuable for your portfolio

This stage makes the project much stronger for your future portfolio.

If you complete it properly, you may later be able to say that you worked on:

- a London transport data engineering project
- local ETL and ELT
- Spark processing
- cloud data lake storage with S3
- layered storage design
- multiple raw source datasets
- structured GitHub documentation

That sounds much more like a real data engineering project than a simple classroom exercise.

This is why your documentation matters.  
This is why your repository structure matters.  
This is why your project notes matter.

---

# 13. How to use this repository

This Day 3 repository is organized into multiple project documents.

Please follow them in order.

## Day 3 documents

- [README 02 - Day 3 Structure and Tasks](./README_02_Day3_Structure_and_Tasks.md)
- [README 03 - Day 3 S3 Setup and Data Lake Layout](./README_03_Day3_S3_Setup_and_Data_Lake_Layout.md)
- [README 04 - Day 3 Spark Data Engineering Tasks](./README_04_Day3_Spark_Data_Engineering_Tasks.md)
- [README 05 - Day 3 Checkpoint Answers](./README_05_Day3_Checkpoint_Answers.md)

Each file has a specific purpose.

Please do not jump randomly between them.

---

# 14. What you should focus on today

For Day 3, focus on:

- understanding the cloud data lake story
- following the S3 setup carefully
- organizing the storage properly
- reading the full raw environment with Spark
- processing all datasets step by step
- writing outputs back to S3
- keeping your notes and repository clean

Do not rush.

The goal is not only to “finish tasks.”

The goal is to understand how a project moves from local processing into a more realistic cloud storage architecture.

---

# 15. Important mindset for Day 3

Please treat this stage like a real engineering upgrade.

That means:

- move slowly
- read carefully
- follow the steps exactly
- do not skip the explanations
- understand what each layer means
- keep your project organized
- push your progress regularly

The project is still guided, but your seriousness and attention still matter.

---

# 16. Final message before starting

Day 3 is where the London Transport project starts to feel much more like a real cloud data engineering project.

On Day 1, you solved the problem locally.  
On Day 2, you rebuilt it with Spark.  
On Day 3, you now engineer the **full raw transport data environment** using **S3 and Spark** in a cloud-style workflow.

That is a big and meaningful step.

Now continue to the next file:

## Next step
- [README 02 - Day 3 Structure and Tasks](./README_02_Day3_Structure_and_Tasks.md)

