#!/bin/bash

docker run -d -p7474:7474 -p7687:7687 -e NEO4J_AUTH=neo4j/s3cr3t neo4j

wget "https://dist.neo4j.org/cypher-shell/cypher-shell_4.2.2_all.deb?_ga=2.114002945.720557071.1620668275-1790379402.1620668275"