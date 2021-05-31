"""
1. Create tests directory in project.
2. Create tests/{resource_name}_tests.py module for each resource.
3. Write test classes in each test module.
4. Create tests/__init__.py module.
5. Import test classes into __init__.py.
6. Run python3 manage.py test tests -v 1 to execute all test classes.

"""
from .game_tests import GameTests
from .event_tests import EventTests
