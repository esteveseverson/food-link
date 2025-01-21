from datetime import datetime


def utc_to_datetime(date: datetime):
    gmt_date = date.strftime('%d/%m/%Y')

    return gmt_date
