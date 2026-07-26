"""Job tracker backend package.

Pure, stdlib-only logic for reading, merging, and writing the job-search data
files (``job_search_tracker.csv`` and ``job_scraper/seen_jobs.json``). The FastAPI
server in ``app.py`` is a thin HTTP layer over these functions; all behaviour here
is importable and unit-testable without starting a server, mirroring
``salary_lookup.py``.
"""
