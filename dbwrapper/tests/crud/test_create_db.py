#import pytest
from dbwrapper import testvalue

def test_create_db():
    assert testvalue == 42
