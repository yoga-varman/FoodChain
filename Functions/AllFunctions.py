import sys
from datetime import datetime
sys.path.append("/home/yogavarman/Projects/FoodChain")

from Config.db import JDBC_URL, DB_PROPERTIES, DATABASE_URL,get_conn

import secrets
import string
import hashlib


def generate_userid(cur):
    count_date = datetime.now().strftime("%Y%m%d")
    cur.execute("""
        INSERT INTO foodchain.idgen (
            count_date,
            req_count
        )
        VALUES (%s, 1)

        ON CONFLICT (count_date)
        DO UPDATE
        SET req_count = foodchain.idgen.req_count + 1
        RETURNING req_count
    """, (count_date,))
    result = cur.fetchone()
    seq = result[0] if result else 1
    return f"{count_date}{seq:02d}"
