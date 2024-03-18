from dbconnector import load_config

from models import ProcessDate, SalesSummary, db
from utils import SQLConnector
# ORDER OF TASKS

# Get config data
config = load_config()

# Connect to SQL database
sql_connector = SQLConnector(config)

# Extract data
# df = sql_connector.run_query_li("SELECT TOP 5 * FROM daily_prices")
table_names_tuple = sql_connector.run_query_li(
    "SELECT table_name FROM INFORMATION_SCHEMA.TABLES"
)

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
