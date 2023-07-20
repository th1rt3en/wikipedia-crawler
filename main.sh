#!/bin/bash
pip install -r requirements.txt
cd src
alembic upgrade head
scrapy crawl wiki
python generate_report.py
