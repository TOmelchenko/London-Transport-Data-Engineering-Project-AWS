# Day 3 S3 Setup and Data Lake Layout  
## London Transport Data Engineering Project

Welcome to the **S3 setup and data lake layout** part of Day 3.

This file will guide you step by step through:

- opening your AWS account
- finding the important account information
- configuring AWS CLI correctly
- testing the connection
- creating your S3 bucket
- creating a cloud folder structure
- uploading all raw files
- checking that everything is in the correct place

This part is very important.

Today, you are not using S3 only as a random storage place.

You are using S3 as the **cloud storage foundation** of your London Transport project.

That is why the storage must be organized carefully.

---

# 1. What is the goal of this part?

The goal of this file is to help you build the **cloud storage layout** of the project.

By the end of this file, you should have:

- access to your AWS account
- AWS CLI configured correctly
- a bucket created in S3
- a clear folder structure inside the bucket
- all 10 raw files uploaded into the correct raw layer
- empty processed and curated folders prepared
- confidence that your cloud data lake layout is ready for Spark

This is a very important foundation for the next step.

---

# 2. What is a data lake layout in simple words?

In simple words, a data lake layout means that we do **not** throw files randomly into cloud storage.

Instead, we organize them into logical layers.

For this beginner project, we will use a simple 3-layer style:

- **raw** → original source data
- **processed** → cleaned and transformed outputs
- **curated** → more business-ready outputs and summaries

This is a very common data engineering idea.

It helps teams understand:
- where original data lives
- where cleaned data goes
- where reporting-ready outputs belong

Amazon S3 is commonly used as the storage foundation for this kind of data lake layout. :contentReference[oaicite:0]{index=0}

---

# 3. Day 3 S3 layout for this project

Your S3 bucket should be organized like this:

```text
s3://your-bucket-name/
│
├── raw/
│   ├── stations/
│   ├── lines/
│   ├── journeys/
│   ├── vehicle_types/
│   ├── operators/
│   ├── zones/
│   ├── disruptions/
│   ├── fares/
│   ├── boroughs/
│   └── schedules/
│
├── processed/
│   ├── stations/
│   ├── lines/
│   ├── journeys/
│   ├── vehicle_types/
│   ├── operators/
│   ├── zones/
│   ├── disruptions/
│   ├── fares/
│   ├── boroughs/
│   ├── schedules/
│   └── joined/
│
└── curated/
    ├── business_reports/
    ├── summaries/
    └── final_outputs/
````

This may look bigger than a simple folder, but that is intentional.

It helps the project feel more like real cloud data engineering.

---

# 4. Before starting

Before doing anything in S3, make sure:

* your AWS account or lab account is ready
* your AWS CLI is installed
* your raw files are already available locally inside:

```text
data/raw/
```

You should have all 10 files:

* `stations.csv`
* `lines.csv`
* `journeys.json`
* `vehicle_types.csv`
* `operators.csv`
* `zones.csv`
* `disruptions.json`
* `fares.csv`
* `boroughs.csv`
* `schedules.xml`

If any file is missing, stop and fix that first.

---

# 5. First open your AWS account in the browser

## Your task

Open the AWS Management Console in your browser.

If your course uses a lab or sandbox account, first open the lab portal and then open AWS from there.

## What you need to find inside AWS

Before configuring AWS CLI, you need to know these things:

* which AWS account you are using
* which AWS Region you should work in
* whether you have **programmatic access credentials**
* whether your course/lab gave you:

  * an **Access Key ID**
  * a **Secret Access Key**
  * or a temporary lab login only

The AWS CLI needs credentials plus a default region to work correctly. AWS’s quick-start guide explains that the basic setup includes credentials, default output format, and default region. ([AWS Documentation][1])

---

# 6. Find your AWS account and region in the console

## Step 1

After opening AWS, look at the **top right area** of the console.

You should usually be able to see:

* your **account name** or account number
* the current **Region**

## Step 2

Write these down in your notes:

* account name or account number
* region name, for example:

  * `eu-central-1`
  * `us-east-1`

## Why this matters

You need the correct region later when configuring AWS CLI and creating S3 resources.

If your course instructor told you to use one specific region, always follow that instruction.

---

# 7. Decide how you will configure AWS CLI

There are two common situations for students.

## Situation A — Your course or lab already gave you access keys

If your instructor or lab system gave you:

* AWS Access Key ID
* AWS Secret Access Key

then you can configure AWS CLI directly.

## Situation B — You only have console login but no access keys

If you can sign in to AWS in the browser, but you do **not** have an Access Key ID and Secret Access Key, then AWS CLI will not work until you receive programmatic credentials or create them in IAM, if your permissions allow it. AWS documents that the AWS CLI needs credential information for programmatic access. ([AWS Documentation][1])

If you are in Situation B, continue to the next section.

---

# 8. If you do not have access keys yet

## Important note

Do **not** create anything randomly.

Only do this if:

* your instructor told you to do it
* or your AWS permissions allow it
* or your lab instructions explicitly expect you to create your own CLI access key

AWS documents that access keys are created from the IAM user’s **Security credentials** page, and that the **secret access key is shown only once at creation time**. ([AWS Documentation][2])

---

# 9. How to create access keys in AWS Console

## Step 1

In the AWS Console, search for:

```text
IAM
```

and open the **IAM** service.

## Step 2

In IAM, go to your user.

Depending on your environment, this may be under:

* **Users**
* or your own IAM user page
* or it may already open directly if the lab uses a simplified account

## Step 3

Open the tab called:

```text
Security credentials
```

## Step 4

Find the section:

```text
Access keys
```

## Step 5

Choose:

```text
Create access key
```

AWS’s IAM user documentation shows that access keys are created from the user’s **Security credentials** page, under **Access keys**. ([AWS Documentation][3])

## Step 6

If AWS asks how the key will be used, choose the option related to:

```text
Command Line Interface (CLI)
```

AWS’s CLI authentication guide specifically describes creating an access key for **Command Line Interface (CLI)** use. ([AWS Documentation][4])

## Step 7

Save both of these immediately:

* **Access Key ID**
* **Secret Access Key**

## Important warning

The **Secret Access Key is shown only one time** when you create it. If you lose it later, you must delete that key and create a new one. ([AWS Documentation][2])

## If you are not allowed to create access keys

Then stop and ask your instructor for help.

Do not try to bypass account rules.

---

# 10. Check whether AWS CLI is installed

## Your task

Run:

```bash
aws --version
```

## What should happen

You should see a version message.

Example:

```text
aws-cli/2.x.x Python/3.x.x ...
```

## If it does not work

Go back to the install steps in `README_02_Day3_Structure_and_Tasks.md` and install AWS CLI first using the official installer steps. AWS provides the official Linux installer process for AWS CLI v2. ([AWS Documentation][1])

Do not continue until this works.

---

# 11. Configure AWS CLI

## Your task

Now run:

```bash
aws configure
```

AWS CLI’s configure command writes the Access Key ID, Secret Access Key, and region to the shared configuration and credentials files. ([AWS Documentation][5])

## You will be asked for 4 things

### 1. AWS Access Key ID

Paste your **Access Key ID**

### 2. AWS Secret Access Key

Paste your **Secret Access Key**

### 3. Default region name

Type your region, for example:

```text
eu-central-1
```

Use the same region you saw in the AWS Console or the one your instructor told you to use.

### 4. Default output format

Type:

```text
json
```

That is a good default for this project.

---

# 12. Check what AWS CLI saved

## Your task

Run:

```bash
aws configure list
```

## What this does

This command shows what AWS CLI is currently using for:

* access key
* secret key
* region

AWS documents that `aws configure list` shows the configuration values and where they came from. ([AWS Documentation][6])

## What you want to see

You want to see that values are present, especially for:

* access key
* secret key
* region

If region is empty, configure it again.

---

# 13. Test your AWS connection

## Your task

Run:

```bash
aws sts get-caller-identity
```

## What this does

This command returns information about the AWS identity currently being used by the CLI.

AWS documents that `get-caller-identity` returns the details of the IAM user or role whose credentials are used for the request. ([AWS Documentation][7])

## What should happen

You should see JSON output with fields like:

* `UserId`
* `Account`
* `Arn`

Example:

```json
{
  "UserId": "AIDASAMPLEUSERID",
  "Account": "123456789012",
  "Arn": "arn:aws:iam::123456789012:user/your-user-name"
}
```

This means your AWS CLI is correctly connected.

## If this fails

Usually it means one of these:

* you entered the wrong access key
* you entered the wrong secret key
* the region is wrong
* your lab session expired
* your account does not allow CLI use yet

If that happens, stop and fix the credentials before continuing.

---

# 14. Write your AWS details in your notes

## Your task

Open:

```text
docs/project_notes.md
```

and write down:

* your AWS account number
* your AWS ARN from `get-caller-identity`
* your chosen region
* whether you used existing access keys or created new ones

## Why this matters

Real engineers document their environment details.

This helps you and your instructor understand what account and region you are really using.

---

# 15. Choose a bucket name

## Your task

Choose a unique bucket name.

A good bucket name could look like this:

```text
london-transport-day3-yourname-2026
```

Example:

```text
london-transport-day3-emily-2026
```

## Important note

S3 bucket names must be globally unique.

That means if someone else already used the same name, AWS will reject it.

So add your name or initials to make it unique.

---

# 16. Create the bucket

## Your task

Replace the bucket name below with your own unique bucket name.

Then run:

```bash
aws s3 mb s3://london-transport-day3-yourname-2026
```

## What this does

This creates your S3 bucket.

## What should happen

You should see a message like:

```text
make_bucket: london-transport-day3-yourname-2026
```

## Important note

If you get a bucket-name error, choose another name and try again.

---

# 17. Check that the bucket exists

## Your task

Run:

```bash
aws s3 ls
```

## What this does

It lists your available S3 buckets.

## What should happen

You should see your new bucket name in the list.

This confirms that the bucket was created successfully.

---

# 18. Create the raw layer folders

## Your task

Now create the raw data folders inside the bucket.

Replace the bucket name with your own.

Run these commands one by one:

```bash
aws s3api put-object --bucket london-transport-day3-yourname-2026 --key raw/stations/
aws s3api put-object --bucket london-transport-day3-yourname-2026 --key raw/lines/
aws s3api put-object --bucket london-transport-day3-yourname-2026 --key raw/journeys/
aws s3api put-object --bucket london-transport-day3-yourname-2026 --key raw/vehicle_types/
aws s3api put-object --bucket london-transport-day3-yourname-2026 --key raw/operators/
aws s3api put-object --bucket london-transport-day3-yourname-2026 --key raw/zones/
aws s3api put-object --bucket london-transport-day3-yourname-2026 --key raw/disruptions/
aws s3api put-object --bucket london-transport-day3-yourname-2026 --key raw/fares/
aws s3api put-object --bucket london-transport-day3-yourname-2026 --key raw/boroughs/
aws s3api put-object --bucket london-transport-day3-yourname-2026 --key raw/schedules/
```

## Why this matters

This creates a clear storage location for each raw source.

Instead of throwing all files into one place, we organize them by dataset.

That is much more professional.

---

# 19. Create the processed layer folders

## Your task

Now create the processed folders:

```bash
aws s3api put-object --bucket london-transport-day3-yourname-2026 --key processed/stations/
aws s3api put-object --bucket london-transport-day3-yourname-2026 --key processed/lines/
aws s3api put-object --bucket london-transport-day3-yourname-2026 --key processed/journeys/
aws s3api put-object --bucket london-transport-day3-yourname-2026 --key processed/vehicle_types/
aws s3api put-object --bucket london-transport-day3-yourname-2026 --key processed/operators/
aws s3api put-object --bucket london-transport-day3-yourname-2026 --key processed/zones/
aws s3api put-object --bucket london-transport-day3-yourname-2026 --key processed/disruptions/
aws s3api put-object --bucket london-transport-day3-yourname-2026 --key processed/fares/
aws s3api put-object --bucket london-transport-day3-yourname-2026 --key processed/boroughs/
aws s3api put-object --bucket london-transport-day3-yourname-2026 --key processed/schedules/
aws s3api put-object --bucket london-transport-day3-yourname-2026 --key processed/joined/
```

## Why this matters

The processed layer is where cleaned and transformed data will go later.

This separation between raw and processed is a very important data engineering habit.

---

# 20. Create the curated layer folders

## Your task

Now create the curated folders:

```bash
aws s3api put-object --bucket london-transport-day3-yourname-2026 --key curated/business_reports/
aws s3api put-object --bucket london-transport-day3-yourname-2026 --key curated/summaries/
aws s3api put-object --bucket london-transport-day3-yourname-2026 --key curated/final_outputs/
```

## Why this matters

The curated layer is for more final, business-ready outputs.

This is where the project starts to feel much more like a real data engineering platform.

---

# 21. Upload the raw files into the correct folders

## Your task

Now upload all raw source files into the correct raw folders.

Make sure you are in the project root first.

Then run:

```bash
aws s3 cp data/raw/stations.csv s3://london-transport-day3-yourname-2026/raw/stations/stations.csv
aws s3 cp data/raw/lines.csv s3://london-transport-day3-yourname-2026/raw/lines/lines.csv
aws s3 cp data/raw/journeys.json s3://london-transport-day3-yourname-2026/raw/journeys/journeys.json
aws s3 cp data/raw/vehicle_types.csv s3://london-transport-day3-yourname-2026/raw/vehicle_types/vehicle_types.csv
aws s3 cp data/raw/operators.csv s3://london-transport-day3-yourname-2026/raw/operators/operators.csv
aws s3 cp data/raw/zones.csv s3://london-transport-day3-yourname-2026/raw/zones/zones.csv
aws s3 cp data/raw/disruptions.json s3://london-transport-day3-yourname-2026/raw/disruptions/disruptions.json
aws s3 cp data/raw/fares.csv s3://london-transport-day3-yourname-2026/raw/fares/fares.csv
aws s3 cp data/raw/boroughs.csv s3://london-transport-day3-yourname-2026/raw/boroughs/boroughs.csv
aws s3 cp data/raw/schedules.xml s3://london-transport-day3-yourname-2026/raw/schedules/schedules.xml
```

## Why this matters

This step brings the full raw transport data environment into cloud storage.

That is one of the most important upgrades of Day 3.

---

# 22. Check the uploaded files in S3

## Your task

Check each raw folder.

Example:

```bash
aws s3 ls s3://london-transport-day3-yourname-2026/raw/stations/
aws s3 ls s3://london-transport-day3-yourname-2026/raw/lines/
aws s3 ls s3://london-transport-day3-yourname-2026/raw/journeys/
aws s3 ls s3://london-transport-day3-yourname-2026/raw/vehicle_types/
aws s3 ls s3://london-transport-day3-yourname-2026/raw/operators/
aws s3 ls s3://london-transport-day3-yourname-2026/raw/zones/
aws s3 ls s3://london-transport-day3-yourname-2026/raw/disruptions/
aws s3 ls s3://london-transport-day3-yourname-2026/raw/fares/
aws s3 ls s3://london-transport-day3-yourname-2026/raw/boroughs/
aws s3 ls s3://london-transport-day3-yourname-2026/raw/schedules/
```

## What should happen

Each command should show the file you uploaded.

If a folder is empty, go back and upload that file again.

---

# 23. View the whole bucket structure

## Your task

Run:

```bash
aws s3 ls s3://london-transport-day3-yourname-2026/ --recursive
```

## What this does

This shows all files and folder objects inside the bucket.

## Why this matters

This helps you confirm that the data lake layout is correct.

It should not look random.

It should look structured.

---

# 24. Write your bucket name in your notes

## Your task

Open:

```text
docs/project_notes.md
```

and write down:

* your bucket name
* the folder structure you created
* that all 10 raw files were uploaded successfully
* what raw / processed / curated means in your own words

## Why this matters

Real engineers document important environment details.

Your notes should help another person understand your project more easily.

---

# 25. What students should understand after this part

By the end of this S3 setup stage, you should understand that:

* AWS CLI must be connected correctly before any S3 work can happen
* S3 is the cloud storage foundation of this project
* raw data should be stored in an organized way
* processed and curated layers should be separated from raw data
* all source files are now part of one cloud storage architecture
* the next Spark step will read from this cloud layout, not only from local folders

That is the main learning goal of this file.

---

# 26. If a file upload fails

If one of your upload commands fails, check:

* are you in the correct project folder?
* does the file really exist in `data/raw/`?
* did you type the filename correctly?
* did you type your bucket name correctly?
* is your AWS CLI connected to the right account?

If the problem continues, copy the exact error message and ask your instructor for help.

Do not guess.

---

# 27. If `aws sts get-caller-identity` fails

If this command fails, check the most common causes:

* wrong Access Key ID
* wrong Secret Access Key
* no default region set
* expired or inactive lab session
* IAM user or role does not allow the action
* typo during `aws configure`

Try these checks:

```bash
aws configure list
aws sts get-caller-identity
```

If the output still fails, go back and reconfigure AWS CLI.

Do not continue to S3 until this is fixed.

---

# 28. Commit and push your progress

## Your task

After completing the S3 setup and data lake layout, push your progress.

Example:

```bash
git add .
git commit -m "Complete Day 3 S3 setup and data lake layout"
git push
```

## Why this matters

Your GitHub repository should reflect your real project progress.

That is part of professional workflow.

---

# 29. Final message before moving on

You have now completed one of the most important foundations of Day 3.

Your cloud storage should now:

* exist in S3
* contain all raw files
* be organized into meaningful layers
* be ready for Spark processing

That is a real upgrade from Day 2.

Now continue to the next file:

## Next step

* [README 04 - Day 3 Spark Data Engineering Tasks](./README_04_Day3_Spark_Data_Engineering_Tasks.md)



[1]: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html "Setting up the AWS CLI - AWS Command Line Interface"
[2]: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html "Manage access keys for IAM users"
[3]: https://docs.aws.amazon.com/IAM/latest/UserGuide/access-key-self-managed.html "How IAM users can manage their own access keys"
[4]: https://docs.aws.amazon.com/cli/v1/userguide/cli-authentication-user.html "Authenticating using IAM user credentials for the AWS CLI"
[5]: https://docs.aws.amazon.com/cli/latest/reference/configure/ "configure — AWS CLI 2.34.10 Command Reference"
[6]: https://docs.aws.amazon.com/cli/v1/userguide/cli-configure-files.html "Configuration and credential file settings in the AWS CLI"
[7]: https://docs.aws.amazon.com/cli/latest/reference/sts/get-caller-identity.html "get-caller-identity — AWS CLI 2.34.10 Command Reference"
