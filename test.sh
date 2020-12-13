#!/bin/sh


echo "0.1.0
0.2.0
0.3.0" | python3 semver-tag.py 0.2.1

echo "0.1.0
0.2.0
0.3.0" | python3 semver-tag.py 0.3.1

echo "0.1.0
0.2.0
0.3.0" | python3 semver-tag.py 1.0.0

echo "0.1.0-snapshot-20201212-137
0.1.0-snapshot-20201212-138
0.1.0-snapshot-20201212-139" | python3 semver-tag.py 0.1.0-snapshot-20201212-140



