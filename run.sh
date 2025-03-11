# amw - 2025-02-18
# This script runs the entire data scrape.
#

'''
Generally, the steps of this scrape are run interactively,
however this script outlines the steps to run the entire scrape.
'''

python3 scripts/scrape.py
python3 scripts/clean.py
python3 scripts/analysis.py
