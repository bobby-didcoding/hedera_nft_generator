# --------------------------------------------------------------
# Python imports
# --------------------------------------------------------------
from pathlib import Path

# --------------------------------------------------------------
# 3rd party imports
# --------------------------------------------------------------
import requests

def add_to_ipfs(filepath, useable_filename):
  '''
  Used to send files to IPFS
  Returns the IFPS URI
  '''
  with Path(filepath).open("rb") as fp:
      image_binary=fp.read()
      url = "http://ipfs:5001/api/v0/add"
      response = requests.post(url, files={"file": image_binary})
      ipfs_hash=response.json()["Hash"]
      ipfs_uri=f"https://ipfs.io/ipfs/{ipfs_hash}"
      return ipfs_uri
