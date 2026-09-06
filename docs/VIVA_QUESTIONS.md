# Viva Questions and Answers

## Basic questions

### 1. What is the project title?

Social Media Trend Analyzer Using Hadoop MapReduce.

### 2. What is the main objective?

To identify frequently occurring keywords and hashtags from a large collection of social-media posts using distributed storage and parallel processing.

### 3. Why did you use Hadoop?

Hadoop provides HDFS for distributed storage and MapReduce for parallel processing of large datasets.

### 4. What dataset did you use?

A deterministic synthetic CSV dataset containing 50,000 social-media posts. It includes post ID, platform, timestamp, and text.

### 5. Why is the dataset synthetic?

It is free, reproducible, contains no private user information, and avoids paid or restricted social-media APIs.

### 6. Can the project use a real dataset?

Yes. An appropriately licensed CSV can replace the generated file as long as the post text is in the final column.

## Hadoop and HDFS

### 7. What is HDFS?

HDFS is the Hadoop Distributed File System. It stores large files as blocks across DataNodes and is managed by the NameNode.

### 8. What is the NameNode?

The NameNode manages HDFS metadata, including file names, directories, permissions, and block locations.

### 9. What is the DataNode?

A DataNode stores the actual HDFS data blocks and reports their status to the NameNode.

### 10. Why is replication set to 1?

This is a single-node educational cluster with only one DataNode. A production cluster normally uses multiple replicas.

### 11. What is pseudo-distributed mode?

All Hadoop services run as separate processes on one machine while behaving like a small Hadoop cluster.

### 12. What is YARN?

YARN manages computing resources and schedules Hadoop applications.

### 13. What is the ResourceManager?

It manages cluster-wide resources and schedules applications.

### 14. What is the NodeManager?

It runs on a worker node and manages the containers that execute tasks.

### 15. Which Hadoop services ran in the project?

NameNode, DataNode, ResourceManager, and NodeManager.

### 16. What does the `jps` command do?

It lists running Java processes, allowing us to verify Hadoop services.

### 17. Why must the NameNode not be formatted repeatedly?

Formatting creates a new HDFS namespace and can make existing HDFS data inaccessible.

## MapReduce

### 18. What is MapReduce?

MapReduce is a distributed programming model consisting of Mapper processing, shuffle and sort, and Reducer aggregation.

### 19. What does your Mapper do?

It parses each post, normalizes text, extracts hashtags and keywords, removes noise and stop words, and emits each item with the value 1.

### 20. Give an example Mapper output.

`K:python\t1` for a keyword and `H:#ai\t1` for a hashtag.

### 21. What is shuffle and sort?

It is Hadoop's automatic phase that transfers, sorts, and groups Mapper output so identical keys reach the same Reducer.

### 22. What does your Reducer do?

It adds all values for each grouped keyword or hashtag and emits the final frequency.

### 23. Why are `K:` and `H:` prefixes used?

They distinguish keywords from hashtags in a single MapReduce output.

### 24. What is Hadoop Streaming?

It allows executable programs that read standard input and write standard output, such as Python scripts, to serve as Mappers and Reducers.

### 25. How was the Mapper and Reducer tested before Hadoop?

They were connected locally with a shell pipeline containing the Mapper, sort, and Reducer and tested on the sample CSV.

## Text processing and results

### 26. What preprocessing was performed?

CSV parsing, lowercasing, URL removal, mention removal, hashtag extraction, word tokenization, and stop-word removal.

### 27. Why convert text to lowercase?

It makes different letter cases count as the same trend, such as `AI`, `Ai`, and `ai`.

### 28. What is a stop word?

A common or context-generic word that does not provide useful trend information, such as “the,” “and,” or “this.”

### 29. What were the top results?

The top keyword was `data` with 15,931 occurrences. The top hashtag was `#artificialintelligence` with 6,297 occurrences.

### 30. How many final reduced records were produced?

The corrected Hadoop run produced 144 reduced output records.

### 31. Were there Hadoop shuffle failures?

No. The job reported zero failed shuffles.

### 32. How were charts created?

A Python script sorted the reducer counts and used Matplotlib to generate horizontal bar charts.

## Design and evaluation

### 33. What are the advantages of this project?

It is scalable, reproducible, free, privacy-safe, and separates distributed processing from visualization.

### 34. What are its limitations?

The dataset is synthetic, frequency does not capture sentiment, phrases are split into individual words, and the demonstration runs on one node.

### 35. How can the project be improved?

It can add real-time data, sentiment analysis, phrase extraction, time-based trends, multilingual processing, Spark, and an interactive dashboard.

### 36. Why not process everything only with Python?

Python can handle the demonstration dataset on one machine, but Hadoop demonstrates distributed storage, task scheduling, parallel processing, and scalability for much larger data.

### 37. How is this a Big Data project if it uses one computer?

The single-node environment demonstrates the same HDFS and MapReduce architecture. On a multi-node cluster, Hadoop can distribute the same Mapper and Reducer without redesigning the algorithm.

### 38. What happens if the output folder already exists?

Hadoop refuses to overwrite a MapReduce output directory. The execution script safely removes only the previous `/social_media/output` directory before a new run.

### 39. Where is the input stored?

The generated CSV is uploaded to `/social_media/input/posts.csv` in HDFS.

### 40. Where are the results stored?

The distributed output is in `/social_media/output`, the merged local count file is `results/trend_counts.tsv`, and the charts are in the `results` folder.

## One-minute explanation

“Our project analyzes social-media posts to find trending keywords and hashtags. We generated 50,000 reproducible synthetic posts and stored them in HDFS. A Python Mapper extracts normalized keywords and hashtags and emits each with a count of one. Hadoop automatically performs shuffle and sort, after which a Python Reducer totals every key. The job is scheduled through YARN and produced 144 reduced records with no failed shuffles. Finally, Python and Matplotlib rank the Top 10 results and create charts. The leading keyword was data, and the leading hashtag was #artificialintelligence. Although we demonstrated it on one node, the same design can scale across a multi-node Hadoop cluster.”
