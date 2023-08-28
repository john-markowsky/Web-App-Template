#test_database.py

import pytest
from database import Item, ActiveHost
from datetime import datetime

def test_create_item(db_session):
    valid_from_date = datetime.strptime("2023-01-01", "%Y-%m-%d")
    valid_until_date = datetime.strptime("2023-12-31", "%Y-%m-%d")
    item = Item(user_id=1, subject="Test Subject", issuer="Test Issuer", valid_from=valid_from_date, valid_until=valid_until_date, status="Valid")
    db_session.add(item)
    db_session.commit()


def test_create_active_host(db_session):
    active_host = ActiveHost(user_id=1, ip_address="192.168.0.1")
    db_session.add(active_host)
    db_session.commit()
    assert active_host.id is not None
