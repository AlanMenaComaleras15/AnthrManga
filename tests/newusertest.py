import os
import uuid
import supabase
from supabase import *
from datetime import datetime
from dotenv import dotenv_values

config = dotenv_values(".env")

url = config["SUPABASE_URL"]
key = config["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

data, count = supabase.table('users').insert({
    "id": str(uuid.uuid4()),
    "activeid": str(uuid.uuid4()),
    "password": hash("TESTPSWD"),
    "email": "alanmena@pm.me",
    "timestamp": str(datetime.now()),
    "subscribed": False,
    "publisher": False
    }).execute()