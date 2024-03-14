import os
from configparser import ConfigParser


def load_config(section: str = 'mssql') -> dict:
    """
    Read configuration data from the database.ini

    Parameters
    -----------

    section: section within the .ini file where the details
        are stored 
    """

    dirname = os.getcwd().replace('\\', '/')
    filepath = os.path.join(dirname, 'database.ini')

    parser = ConfigParser()
    parser.read(filepath)

    # Get section in .ini file [section]

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
