# Day 3 Structure and Tasks  
## London Transport Data Engineering Project

Welcome to **Day 3** of the London Transport Data Engineering Project.

This document explains:

- the structure of the Day 3 repository
- the technical setup path for Windows and macOS students
- how to install missing tools such as **AWS CLI** and **PySpark**
- what you must complete today
- how the S3 + Spark stage is organized
- what your deliverables are by the end of Day 3

Please read this file carefully before starting the S3 and Spark task files.

---

# 1. Day 3 goal

The goal of **Day 3** is to complete the **cloud data lake stage** of the London Transport Data Engineering Project.

That means by the end of today, you should have:

- a working Day 3 GitHub repository
- the correct folder structure
- access to the raw data files
- **AWS CLI** working in your environment
- **Spark / PySpark** working in your environment
- all raw files uploaded to **S3**
- a clear **raw / processed / curated-style storage layout**
- Spark reading data from **S3**
- processed outputs written back to **S3**
- checkpoint answers written
- your progress pushed to GitHub step by step

This is a full project day, and it should feel like a real junior data engineering task.

---

# 2. Day 3 project scope

For **Day 3 only**, your work is focused on:

- **S3 as cloud storage**
- **Spark as the processing engine**
- **all raw files** in the transport project
- **cloud data lake style organization**

You are **not** working on:

- Glue Catalog
- Athena
- Databricks
- orchestration tools
- dashboards

Today is about taking the full London Transport raw data environment and engineering it in a **cloud-style S3 + Spark workflow**.

---

# 3. What Day 3 is trying to teach you

Day 3 is here to help you understand that a data engineering project becomes more realistic when it moves from local files into structured cloud storage.

On Day 1, you solved the problem locally with:
- Python
- PostgreSQL
- ETL
- ELT

On Day 2, you solved the same business problem with:
- Spark
- Spark DataFrames
- Spark joins
- Spark aggregations

On Day 3, you now solve it as a **cloud data lake workflow** with:
- S3
- Spark
- all raw datasets
- layered storage design

This is important because real data engineering work is not only about local scripts.  
It is also about how data is stored, organized, moved, and processed in cloud environments.

---

# 4. Full raw data for Day 3

For Day 3, you will work with the **full raw source layer**.

That means all of these files are in scope:

```text
data/raw/
├── stations.csv
├── lines.csv
├── journeys.json
├── vehicle_types.csv
├── operators.csv
├── zones.csv
├── disruptions.json
├── fares.csv
├── boroughs.csv
└── schedules.xml
````

Today, you should not think only about a few files.

The idea of Day 3 is that you are engineering the **full raw transport data environment** in cloud storage.

---

# 5. Day 3 repository structure

Your Day 3 repository should look like this:

```text
london-transport-cloud-data-lake-project/
│
├── README.md
├── README_02_Day3_Structure_and_Tasks.md
├── README_03_Day3_S3_Setup_and_Data_Lake_Layout.md
├── README_04_Day3_Spark_Data_Engineering_Tasks.md
├── README_05_Day3_Checkpoint_Answers.md
│
├── data/
│   ├── raw/
│   │   ├── stations.csv
│   │   ├── lines.csv
│   │   ├── journeys.json
│   │   ├── vehicle_types.csv
│   │   ├── operators.csv
│   │   ├── zones.csv
│   │   ├── disruptions.json
│   │   ├── fares.csv
│   │   ├── boroughs.csv
│   │   └── schedules.xml
│   └── output/
│
├── src/
│   ├── cloud_pipeline.py
│   └── utils.py
│
├── docs/
│   ├── project_notes.md
│   └── checkpoint_answers.md
│
├── logs/
│   └── spark.log
│
└── requirements.txt
```

This structure is simple, but still professional.

It helps separate:

* raw data
* Spark code
* documentation
* outputs
* logs

That is a good engineering habit.

---

# 6. Why this structure matters

A good cloud data engineering project should not be a random collection of files.

Even when the work is guided, your repository should still look organized and professional.

This structure makes the project:

* easier to understand
* easier to run
* easier to explain
* easier to show later in interviews

This is important because the value of this project is not only the code.
It is also how clearly and professionally it is presented.

---

# 7. Environment setup path for students

Because students use different operating systems, the beginning of the setup is slightly different.

## Windows students

Windows students should begin from:

* **Git Bash**
* then enter **WSL**
* then continue the project inside WSL

## macOS students

macOS students should begin from:

* **Terminal**
* then continue directly into the project

After those environment-specific starting steps, everyone should continue with the **same Day 3 workflow**.

That means the technical beginning is different, but the main Day 3 tasks are shared by everyone.

---

# 8. Windows students - how to begin

If you are a Windows student, start like this:

## Step 1

Open **Git Bash**

## Step 2

Enter WSL

```bash
wsl
```

## Step 3

Move to the correct folder where your Day 3 repository is stored

Example:

```bash
cd /mnt/c/Users/YourName/path/to/london-transport-cloud-data-lake-project
```

## Step 4

Check that you are in the correct project folder

```bash
pwd
ls
```

You should see your README files, `src`, `data`, and `docs`.

---

# 9. macOS students - how to begin

If you are a macOS student, start like this:

## Step 1

Open **Terminal**

## Step 2

Move into your Day 3 project folder

Example:

```bash
cd /path/to/london-transport-cloud-data-lake-project
```

## Step 3

Confirm you are in the correct location

```bash
pwd
ls
```

You should see your README files, `src`, `data`, and `docs`.

---

# 10. Common setup for everyone after that

From this point onward, all students should continue with the same workflow.

## Step 1

Check Python version

```bash
python3 --version
```

## Step 2

Check Java version

```bash
java -version
```

Spark needs Java, so this is important.

## Step 3

Check whether AWS CLI is available

```bash
aws --version
```

## Step 4

Check whether PySpark is available

```bash
pyspark
```

If PySpark opens, that is a good sign.

To exit:

```python
exit()
```

or press:

```text
Ctrl + D
```

If something is missing, do not panic.
Follow the installation sections below.

---

# 11. If AWS CLI is not installed

If this command does not work:

```bash
aws --version
```

follow these steps carefully.

## Step 1 - Install unzip if missing

In WSL or Ubuntu:

```bash
sudo apt update
sudo apt install unzip -y
```

In macOS, if `unzip` is missing, it is usually already available. If not, ask for help before continuing.

## Step 2 - Download the AWS CLI installer

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
```

## Step 3 - Unzip the installer

```bash
unzip awscliv2.zip
```

## Step 4 - Run the installer

```bash
sudo ./aws/install
```

## Step 5 - Check it again

```bash
aws --version
```

If it now prints a version, the installation worked.

## Important note for students with `sudo` disabled

If `sudo` is disabled on your machine, please do **not** keep trying random installation commands.

Instead:

* ask the instructor for help
* share your screen
* show the exact error message

Do not guess.

---

# 12. If PySpark is not installed

If this command does not work:

```bash
pyspark
```

follow these steps carefully.

## Step 1 - Move into your project folder

```bash
cd /path/to/your/project
```

## Step 2 - Create a virtual environment

```bash
python3 -m venv env
```

## Step 3 - Activate it

```bash
source env/bin/activate
```

After activation, you should see `(env)` at the beginning of the line.

## Step 4 - Upgrade pip

```bash
pip install --upgrade pip
```

## Step 5 - Install PySpark

```bash
pip install pyspark
```

## Step 6 - Test it

```bash
pyspark
```

If it opens, then PySpark is installed correctly.

To exit:

```python
exit()
```

## If `pyspark` still says command not found

Try:

```bash
python -m pyspark
```

---

# 13. If Java is not found

If this command fails:

```bash
java -version
```

then Spark will not work.

## For Windows + WSL students

First, check whether Java exists on the **Windows host**.

Inside WSL, run:

```bash
cmd.exe /c "where java"
```

If it returns a Windows path like:

```text
C:\Program Files\Java\jdk-17\bin\java.exe
```

then you can use that Java from inside WSL.

Set `JAVA_HOME` like this:

```bash
export JAVA_HOME="/mnt/c/Program Files/Java/jdk-17"
export PATH="$JAVA_HOME/bin:$PATH"
java -version
```

If that works, save it permanently:

```bash
nano ~/.bashrc
```

Add these lines at the end:

```bash
export JAVA_HOME="/mnt/c/Program Files/Java/jdk-17"
export PATH="$JAVA_HOME/bin:$PATH"
```

Then run:

```bash
source ~/.bashrc
```

## If Java is not installed on Windows either

Then the student cannot fix it alone without admin rights.

In that case:

* ask the instructor for help
* or use a machine where Java is already available
* or pair temporarily with another student

Do not waste time guessing.

---

# 14. If VS Code cannot open the WSL folder

If a Windows student cloned the repo in WSL and sees a message that the location cannot be opened from Windows VS Code normally, use this method.

## Step 1

Inside WSL, move into the project folder:

```bash
cd /path/to/your/project
```

## Step 2

Run:

```bash
code .
```

This should open the folder in Windows VS Code using the WSL connection.

## Step 3

If `code .` does not work
Install the VS Code extension:

* **Remote - WSL**

Then close and reopen VS Code, return to WSL, and run:

```bash
code .
```

This is the correct way to open a WSL-based project in VS Code.

---

# 15. Suggested Day 3 task list

Here is what you must complete today.

## Task 1 — Read the Day 3 main README

Read `README.md` and understand:

* what Stage 3 is
* how it connects to Day 1 and Day 2
* why this stage is a cloud data lake upgrade

## Task 2 — Confirm your environment

Make sure you can:

* open the correct terminal
* move into the correct project folder
* check Python and Java
* check AWS CLI
* check PySpark

## Task 3 — Install missing tools if needed

If:

* AWS CLI is missing → follow the AWS CLI install steps
* PySpark is missing → follow the PySpark install steps
* Java is missing → follow the Java section or ask for help

## Task 4 — Confirm the project structure

Make sure the Day 3 repository has the correct folders and files.

## Task 5 — Confirm the raw data files

Make sure all raw files are inside:

```text
data/raw/
```

## Task 6 — Complete the S3 setup tasks

Follow:

* [README 03 - Day 3 S3 Setup and Data Lake Layout](./README_03_Day3_S3_Setup_and_Data_Lake_Layout.md)

## Task 7 — Complete the Spark data engineering tasks

Follow:

* [README 04 - Day 3 Spark Data Engineering Tasks](./README_04_Day3_Spark_Data_Engineering_Tasks.md)

## Task 8 — Write project notes

Add notes to:

```text
docs/project_notes.md
```

You should write short notes about:

* how the S3 layout was organized
* how all raw files were used
* how Spark processed the cloud data
* what outputs were created
* what felt new compared to Day 2

## Task 9 — Answer checkpoint questions

Complete:

```text
docs/checkpoint_answers.md
```

## Task 10 — Commit and push progress

Push your progress regularly to your GitHub repository.

---

# 16. Suggested Day 3 commit milestones

To help you stay organized, here are some good commit points for today.

## Commit 1

After repository setup and environment check

Example:

```bash
git commit -m "Set up Day 3 cloud data lake repository and environment"
```

## Commit 2

After confirming the raw data files

```bash
git commit -m "Add Day 3 raw data files"
```

## Commit 3

After S3 bucket and folder layout setup

```bash
git commit -m "Set up S3 data lake layout"
```

## Commit 4

After starting Spark cloud data loading

```bash
git commit -m "Start Spark processing from S3"
```

## Commit 5

After finishing processed outputs and checkpoint answers

```bash
git commit -m "Complete Day 3 cloud data lake deliverables"
```

These are examples, but they show how to work in a structured way.

---

# 17. What students should focus on technically today

The most important technical ideas of Day 3 are:

* cloud storage structure
* S3 bucket and folder organization
* raw / processed / curated thinking
* reading data from S3 with Spark
* cleaning and transforming all datasets
* producing outputs back into S3
* understanding how cloud storage changes the workflow

This is not meant to be random cloud experimentation.

It is a guided workflow, so the goal is to understand each step clearly.

---

# 18. What students should observe while working

As you work today, think about these questions:

* How does S3 change the project compared to Day 2?
* Why is cloud storage more realistic than only local folders?
* What does it mean to use all raw files in one cloud data lake workflow?
* Why do engineers separate raw, processed, and curated layers?
* How does Spark fit into that storage architecture?

These reflections are important because they connect tool usage to real engineering thinking.

---

# 19. Day 3 deliverables

By the end of Day 3, your repository should contain:

* your own public GitHub Day 3 repository
* all 5 Day 3 README files
* the correct project structure
* the raw data files
* S3 bucket and folder organization
* a working Spark cloud pipeline
* processed outputs
* project notes
* checkpoint answers
* multiple commits showing step-by-step progress

If these are missing, your Day 3 submission is incomplete.

---

# 20. Why this day is important professionally

Day 3 helps you move from:

* local raw files
* local Spark
* local project folders

into:

* cloud storage
* layered data lake thinking
* cloud-connected Spark processing
* full raw data environment engineering

That is a major upgrade in the project story.

A project that includes:

* local ETL / ELT
* local Spark
* S3 cloud data lake design
* full multi-file processing
* structured GitHub documentation

already sounds much more like a real data engineering portfolio project.

---

# 21. Required checkpoint file

For Day 3, you must also complete the checkpoint answers file.

You will find or create it here:

```text
docs/checkpoint_answers.md
```

This file is mandatory.

It helps confirm that you understood:

* the purpose of the S3 + Spark stage
* how it connects to the full project
* the main technical ideas from today

---

# 22. Important reminder

This project is **guided**.

You are not expected to invent everything from scratch.

You are expected to:

* follow the steps carefully
* run the provided logic
* understand what each step is doing
* write notes clearly
* keep your GitHub repository organized

That is the right way to learn from this kind of project.

---

# 23. Final message before starting Day 3 tasks

Day 3 is an important step in the full-stack journey of this project.

On the previous days, you solved the business problem locally and then with Spark.

Today, you will move into a much more realistic cloud data engineering workflow using:

* **S3**
* **Spark**
* **all raw files**
* **cloud storage layers**

That is exactly what makes this project feel stronger, richer, and more professional.

Now continue to the next file:

## Next step

* [README 03 - Day 3 S3 Setup and Data Lake Layout](./README_03_Day3_S3_Setup_and_Data_Lake_Layout.md)

[1]: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html "Installing or updating to the latest version of the AWS CLI"


