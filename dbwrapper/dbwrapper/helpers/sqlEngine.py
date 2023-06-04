from sqlalchemy import create_engine
#from ...constants import connectionString
from ..constants import connectionString
# import os
# import sys

# # Get the absolute path of the current script
# current_path = os.path.abspath(sys.argv[0])
# current_path = os.path.abspath(__file__)

# # Get the directory of the current script
# directory = os.path.dirname(current_path)

# # Print the current execution path
# print("Current execution path:", directory)
# print(f" current_path={current_path}")
# print(f" ConnectionString={connectionString}")

# # Get the path of the currently running Python module
# current_path = os.path.abspath(__file__)

# # Get the directory of the current module
# directory = os.path.dirname(current_path)

# # Get the path to the root of the current package
# package_root = os.path.dirname(directory)

# # Print the path to the root of the current package
# print(" Path to the root of the current package: ", package_root)
engine = create_engine(connectionString, echo=False)
