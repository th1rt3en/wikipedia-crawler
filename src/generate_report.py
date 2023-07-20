import os
import google.auth

from db import Session
from sqlalchemy import text

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID", "1EgkZSKpqX5ZY5Rc_6pl17FxqcBstSArFFuh7XAYxJpA")


def update_values(spreadsheet_id, range_name, value_input_option,  values):
    creds, _ = google.auth.default()
    try:
        service = build("sheets", "v4", credentials=creds)
        body = {
            "values": values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption=value_input_option, body=body).execute()
        print(f"{result.get('updatedCells')} cells updated.")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


def get_common_highest_freq():
    with Session.begin() as sess:
        result = sess.execute(text(open("sql/common_highest_freq.sql", "r").read())).first()
        return result[0], result[1]


def get_avg_freq():
    with Session.begin() as sess:
        result = sess.execute(text(open("sql/average_freq_count.sql", "r").read())).all()
        return [[r[0], r[1]] for r in result]


if __name__ == "__main__":
    # Update sheet with highest common frequency
    word, count = get_common_highest_freq()
    update_values(SPREADSHEET_ID, "Sheet1!A1:C2", "RAW", [
        ["", "Word", "Count"],
        ["Highest common frequency count", word, count]
    ])

    # Update sheet with table of average frequency in DESC order
    update_values(SPREADSHEET_ID, "Sheet1!A4:B4", "RAW", [["Word", "Average Count"]])
    avg_freq = get_avg_freq()
    update_values(SPREADSHEET_ID, "Sheet1!A5:B", "RAW", avg_freq)

    # Insert chart
    creds, _ = google.auth.default()
    try:
        service = build("sheets", "v4", credentials=creds)
        
        requests = []
        requests.append({
            "addChart": {
                "chart": {
                    "chartId": 0,
                    "spec": {
                        "title": "Average Word Frequency",
                        "basicChart": {
                            "chartType": "BAR",
                            "series": [{
                                "series": {
                                    "sourceRange": {
                                        "sources": [{
                                            "sheetId": 0,
                                            "startRowIndex": 4,
                                            "endRowIndex": 24,
                                            "startColumnIndex": 1,
                                            "endColumnIndex": 2
                                        }]
                                    }
                                }
                            }],
                            "domains": [{
                                "domain": {
                                    "sourceRange": {
                                        "sources": [{
                                            "sheetId": 0,
                                            "startRowIndex": 4,
                                            "endRowIndex": 24,
                                            "startColumnIndex": 0,
                                            "endColumnIndex": 1
                                        }]
                                    }
                                }
                            }]
                        }
                    },
                    "position": {
                        "overlayPosition": {
                            "anchorCell": {
                                "sheetId": 0,
                                "rowIndex": 0,
                                "columnIndex": 5
                            }
                        }
                    }
                }
            }
        })
        body = {
            "requests": requests
        }
        response = service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body).execute()
    except HttpError as error:
        print(f"An error occurred: {error}")

