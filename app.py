from dbconnector import load_config

from utils import SQLConnector
# ORDER OF TASKS

# Get config data
config = load_config()

# Connect to SQL database
sql_connector = SQLConnector(config)

# Extract data
# df = sql_connector.run_query_li("SELECT TOP 5 * FROM daily_prices")
df = sql_connector.run_query_li(
    "SELECT table_name FROM INFORMATION_SCHEMA.TABLES")

for tname in df:
    print(tname[0])
# print(df.fetchall())

sql_connector.close_all()
