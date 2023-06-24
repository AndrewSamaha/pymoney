import pytest
import os
from dbwrapper import testvalue
from dbwrapper.constants import getConnectionString, getSeedFolder
from dbwrapper.helpers import seed_worker, getSeedEngine
from dbwrapper.models import Base

envs = [
    'Test',
    'local',
    'default'
]

def test_getConnectionString(snapshot):
    for env in envs:
        cString = getConnectionString(env)
        envCStringPair = f"{env} == {cString}"
        assert envCStringPair == snapshot

def test_getSeedFolder(snapshot):
    for env in envs:
        result = getSeedFolder(env)
        inputResultPair = f"{env} == {result}"
        assert inputResultPair == snapshot
