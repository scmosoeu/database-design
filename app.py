from dbconnector import load_config
from resources import create_app
from resources.extensions import db
from sqlalchemy.exc import IntegrityError

from models import (
    ProcessDate, Product, Container, ProductCombination, ProductSales
)
from utils import SQLConnector


def normalize_data():
    # ORDER OF TASKS

    # Get config data
    config = load_config()

    # Connect to SQL database
    sql_connector = SQLConnector(config)

    # Check processed dates in the data
    process_dates = sql_connector.run_query(
        "SELECT information_date FROM process_date"
    )
    # Query dates when data was extracted
    extract_dates = sql_connector.run_query(
        "SELECT information_date FROM extract_date ORDER BY information_date"
    )
    # Pull dates when the data was extracted
    extracted_dates = [extract_date[0] for extract_date in extract_dates]

    if len(process_dates):
        # Pull dates when the data was processed
        processed_dates = [process_date[0] for process_date in process_dates]
        selected_dates = list(set(extracted_dates) - set(processed_dates))
        for selected_date in selected_dates:
            process_date = ProcessDate(information_date=selected_date)
            db.session.add(process_date)
            db.session.commit()

            with open('sql_scripts/delta_ingestion.sql', 'r') as sql_script:
                script = sql_script.read()
                sales = sql_connector.run_query(script.format(selected_date))
                for sale in sales:
                    # Check if product, container, and combination exist before adding
                    commodity = Product.query.filter_by(
                        commodity=sale[1]).first()
                    if not commodity:
                        commodity = Product(commodity=sale[1])
                        db.session.add(commodity)

                    container = Container.query.filter_by(
                        container=sale[2]).first()
                    if not container:
                        container = Container(container=sale[2])
                        db.session.add(container)

                    combination = ProductCombination.query.filter_by(
                        combination=sale[3]).first()
                    if not combination:
                        combination = ProductCombination(combination=sale[3])
                        db.session.add(combination)

                    # Commit the changes to avoid duplicate inserts
                    db.session.commit()

                    process_sales = ProductSales(
                        information_date=sale[0],
                        products=commodity,
                        containers=container,
                        combinations=combination,
                        total_value_sold=sale[4],
                        total_quantity_sold=sale[5],
                        total_kg_sold=sale[6]
                    )

                    db.session.add(process_sales)

                    db.session.commit()

    else:
        for extracted_date in extracted_dates:
            # Processing the date column
            process_date = ProcessDate(information_date=extracted_date)
            db.session.add(process_date)

        with open('sql_scripts/initial_ingestion.sql', 'r') as sql_script:
            sales = sql_connector.run_query(sql_script.read())
            for sale in sales:
                # Check if product, container, and combination exist before adding
                commodity = Product.query.filter_by(commodity=sale[1]).first()
                if not commodity:
                    commodity = Product(commodity=sale[1])
                    db.session.add(commodity)

                container = Container.query.filter_by(
                    container=sale[2]).first()
                if not container:
                    container = Container(container=sale[2])
                    db.session.add(container)

                combination = ProductCombination.query.filter_by(
                    combination=sale[3]).first()
                if not combination:
                    combination = ProductCombination(combination=sale[3])
                    db.session.add(combination)

                # Commit the changes to avoid duplicate inserts
                db.session.commit()

                process_sales = ProductSales(
                    information_date=sale[0],
                    products=commodity,
                    containers=container,
                    combinations=combination,
                    total_value_sold=sale[4],
                    total_quantity_sold=sale[5],
                    total_kg_sold=sale[6]
                )

                db.session.add(process_sales)

                db.session.commit()

    sql_connector.close_all()


if __name__ == '__main__':
    # Initialize Flask app
    app = create_app()
    with app.app_context():
        normalize_data()
