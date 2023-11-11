
--- Python Job Template v1 ----------------------------------------
- main.py: The fundamental file that is executed at runtime. All the orchestatrion happens here.
- sqlqueries.py: Contains all the queries called by main.py. Each query is a multi-line string variable in the file. Very short queries (e.g. drop table) can be executed directly in main, no need to be added in this.
- run.bat: Executable that calls python with required arguments. Also, it extracts the current month's pattern in order to log the stdout in separate monthly files. Runs with the default parameter values as defined in main.py.
- manual_run.bat: Same as above but it asks for parameter values in the console upon execution. Helpful for manually running the job for past dates and such.
- ddl_citus.sql: All create statements needed on the citus side. Those are statements that run just once when building the job (e.g.creating a fact table that doesn't get rebuild upon execution).
- ddl_hive.sql: As above for Hive
- README.txt: Any other free-form information about the job, changelog, etc
- data (folder): Any data files exchange should happen in this folder, e.g. exporting csv from DB to upload to FTP, caching dataframes in files, etc. This folder of course is git-ignored, since data should be added in the repo. The job should make sure tha this folder doesn;t get filled up with data (temp files should be deleted).
- YYYYMM.log (in data folder): logfile with the stdout of the bat file. The relevant argument in the python call writes in this file in real time, rather than keep it in the buffer. You just need to re-open the file to see fresh logs while the job is running.

--- ETL job guidelines -------------------------------------------
1. Use plenty of comments in the code, the more the better. Make sure they're up to date; same goes for job metadata
2. A job should have the ability to be re-run at any time, regardless of whether it failed and which step it failed at without conflicts on existing tables, files, etc
3. A job should have date (and possibly other types of) parameters which should be clearly declared and documented at the start of the job
4. If it makes sense for a specific job, and performance isn't an issue, the job should cover/ overwrite the last X days. This way, it should be able to recover missing days automaticall in the next run
6. If applicable, date periods should be run in a loop, one day at a time. This means the the date parameters should be at least 2 (min date, max date).
7. Make sure that the log func is called before every significant work item, in order to understand where the job failed exactly and how long steps take when analyzing performance.
8. Unless there's a specific reason, the job should not leave "garbage" in the data folder. Always clean it up or have a retention policy to avoid flooding.
9. Wherever applicable, use funcs that log how many data were processed (e.g. sql_to_csv shows how many records were exported or you could print the length of a dataframe)
10. For jobs where we need to upload files to sftp/gcloud/etc we should do this at the very end and if the upload failes we shouldn't delete the files, so we can manually upload them
11. Variable names should not be correlated to the value they hold, never use "today_minus_seven", "last_15_days", etc
