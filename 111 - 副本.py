from getpass import getpass
import os
FIREWORKS_API_KEY = getpass('sk-qullgfjnwatfbztwedpwajnagikznfbimlotgxhlloyrbkax ')
os.environ["FIREWORKS_API_KEY"] = FIREWORKS_API_KEY
DEEPSEEK_API_KEY = getpass('sk-qullgfjnwatfbztwedpwajnagikznfbimlotgxhlloyrbkax ')
os.environ["DEEPSEEK_API_KEY"] = DEEPSEEK_API_KEY
os.environ["GET_REASONING_CONTENT"]="True"