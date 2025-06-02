from dotenv import load_dotenv
import os 

load_dotenv()

class Config:
    CONVOSO_TOKEN = os.getenv("CONVOSO_TOKEN")
    test_value = "This is a set"

    
