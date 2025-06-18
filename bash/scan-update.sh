#!/bin/bash
echo "[+] Pulling latest data..."
git pull

echo "[+] Running GitHub scanner..."
python3 github_scanner.py

echo "[+] Adding updated resources to git..."
git add github-resources.csv
git commit -m "Update GitHub resources list"
git push
