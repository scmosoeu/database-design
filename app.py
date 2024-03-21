from dbconnector import load_config
from resources import create_app
from resources.extensions import db

from models import ProcessDate, Product, ProductCombination, ProductSales
from utils import SQLConnector


def normalize_data():
    # ORDER OF TASKS

    # Get config data
    config = load_config()

    # Connect to SQL database
    sql_connector = SQLConnector(config)

    # Check processed dates in the data
    process_dates = sql_connector.run_query(
        "SELECT information_date FROM process_date")
    # Query dates when data was extracted
    extract_dates = sql_connector.run_query(
        "SELECT information_date FROM extract_date ORDER BY information_date")
    # Pull dates when the data was extracted
    extracted_dates = [extract_date[0] for extract_date in extract_dates]

    if len(process_dates):
        # Pull dates when the data was processed
        processed_dates = [process_date[0] for process_date in process_dates]
        selected_dates = list(set(extracted_dates) - set(processed_dates))
        for selected_date in selected_dates:
            process_date = ProcessDate(information_date=selected_date)
            db.session.add(process_date)

    else:
        for extracted_date in extracted_dates:
            process_date = ProcessDate(information_date=extracted_date)
            db.session.add(process_date)

    db.session.commit()

    sql_connector.close_all()


if __name__ == '__main__':
    # Initialize Flask app
    app = create_app()
    with app.app_context():
        normalize_data()
