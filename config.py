import os
import fastf1

# Example data for dropdowns
YEARS = list(range(2018, 2025))
SESSIONS = ['FP1', 'FP2', 'FP3', 'Q', 'R']

# Ensure cache directory exists
CACHE_DIR = 'cache'
os.makedirs(CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(CACHE_DIR)  # Enable caching
