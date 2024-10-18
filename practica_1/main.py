import requests
import tomllib
from pathlib import Path

with open("configuracion_p1.toml", "rb") as f:
    conf = tomllib.load(f)

r = requests.get(conf.get("url_servidor"))

dir_cache = Path("cache")
dir_cache.mkdir(exist_ok=True)

cache_file = dir_cache / "index.html"
cache_file.write_text(r.text, encoding='utf-8', errors='ignore')
print("done")
