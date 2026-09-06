#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${PROJECT_ROOT}"

INPUT_FILE="${1:-data/generated_posts.csv}"
HDFS_INPUT="/social_media/input"
HDFS_OUTPUT="/social_media/output"
LOCAL_RESULTS="results/trend_counts.tsv"

if [[ ! -f "${INPUT_FILE}" ]]; then
    echo "Input file not found: ${INPUT_FILE}" >&2
    exit 1
fi

for service in NameNode DataNode ResourceManager NodeManager; do
    if ! jps | awk '{print $2}' | grep -qx "${service}"; then
        echo "${service} is not running." >&2
        exit 1
    fi
done

STREAMING_JAR="$(find "${HADOOP_HOME}/share/hadoop/tools/lib" -name 'hadoop-streaming-*.jar' | head -n 1)"
if [[ -z "${STREAMING_JAR}" ]]; then
    echo "Hadoop Streaming JAR was not found." >&2
    exit 1
fi

hdfs dfs -mkdir -p "${HDFS_INPUT}"
hdfs dfs -rm -f "${HDFS_INPUT}/posts.csv" >/dev/null 2>&1 || true
hdfs dfs -put "${INPUT_FILE}" "${HDFS_INPUT}/posts.csv"
hdfs dfs -rm -r -f "${HDFS_OUTPUT}" >/dev/null 2>&1 || true

hadoop jar "${STREAMING_JAR}" \
    -D mapreduce.job.name="Social Media Trend Analysis" \
    -files mapper.py,reducer.py \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py" \
    -input "${HDFS_INPUT}/posts.csv" \
    -output "${HDFS_OUTPUT}"

mkdir -p results
hdfs dfs -cat "${HDFS_OUTPUT}"/part-* > "${LOCAL_RESULTS}"

echo "MapReduce completed successfully."
echo "Counts saved to ${LOCAL_RESULTS}"
