from subprocess import call
import os 
from pyngrok import ngrok
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# from app import front_main 
call(f"ngrok authtoken {os.environ["MFS_NGROK_TOKEN"]}", shell=True)
call("screen streamlit run mfs/front_main.py &", shell=True)

url = ngrok.connect(port = 8501)

print(url)
#used for starting our server
call("streamlit run --server.port 80 mfs/front_main.py >/dev/null", shell=True)
