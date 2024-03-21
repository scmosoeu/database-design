from .dbconnector import load_config

from .models import ProcessDate, Product, ProductCombination, ProductSales, db, app
from .utils import SQLConnector
# ORDER OF TASKS

# Get config data
config = load_config()

# Connect to SQL database
sql_connector = SQLConnector(config)

# Check processed dates in the data
process_dates = sql_connector.run_query("SELECT * FROM process_date")
# Query dates when data was extracted
extract_dates = sql_connector.run_query("SELECT * FROM extract_date")
# Pull dates when the data was extracted
extracted_dates = [extract_date[0] for extract_date in extract_dates]

if len(process_dates):
    # Pull dates when the data was processed
    processed_dates = [process_date[0] for process_date in process_dates]
    selected_dates = list(set(extracted_dates) - set(process_dates))
    for selected_date in selected_dates:
        process_date = ProcessDate(information_date=selected_date)
        db.session.add(process_date)

    db.session.commit()

else:
    for extracted_date in extracted_dates:
        process_date = ProcessDate(information_date=extracted_date)
        db.session.add(process_date)

    db.session.commit()

# Dates to normalize data for
# unprocessed_dates =

# Insert data into a normalised database

# table_names = [tname[0] for tname in table_names_tuple]
# if 'process_date' not in table_names:
#     extract_dates = sql_connector.run_query_li(
#         "SELECT * FROM extract_date ORDER BY information_date ASC"

#     for extract_date in extract_dates:
#         process_date = ProcessDate(
#             information_date=extract_date[0]
#         )
#         db.session.add(process_date)

#     db.session.commit()

sql_connector.close_all()
