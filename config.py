from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    CONVOSO_TOKEN = os.getenv("CONVOSO_TOKEN")
    ASSEMBLY_TOKEN = os.getenv("ASSEMBLY_TOKEN")
    test_value = "This is a set"
