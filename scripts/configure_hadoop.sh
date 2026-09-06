#!/usr/bin/env bash
set -euo pipefail

HADOOP_HOME="${HADOOP_HOME:-/workspaces/hadoop-3.4.3}"
JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_DIR="${PROJECT_ROOT}/hadoop-config"

if [[ ! -d "${HADOOP_HOME}" ]]; then
    echo "Hadoop was not found at ${HADOOP_HOME}." >&2
    exit 1
fi

mkdir -p /workspaces/hadoop_data/namenode
mkdir -p /workspaces/hadoop_data/datanode
mkdir -p /workspaces/hadoop_data/tmp

cp "${CONFIG_DIR}/core-site.xml" "${HADOOP_HOME}/etc/hadoop/core-site.xml"
cp "${CONFIG_DIR}/hdfs-site.xml" "${HADOOP_HOME}/etc/hadoop/hdfs-site.xml"
cp "${CONFIG_DIR}/mapred-site.xml" "${HADOOP_HOME}/etc/hadoop/mapred-site.xml"
cp "${CONFIG_DIR}/yarn-site.xml" "${HADOOP_HOME}/etc/hadoop/yarn-site.xml"

for env_file in hadoop-env.sh mapred-env.sh yarn-env.sh; do
    target="${HADOOP_HOME}/etc/hadoop/${env_file}"
    if ! grep -qxF "export JAVA_HOME=${JAVA_HOME}" "${target}"; then
        printf '\nexport JAVA_HOME=%s\n' "${JAVA_HOME}" >> "${target}"
    fi
done

echo "Hadoop configuration installed successfully."
