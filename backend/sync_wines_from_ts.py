import re
import json
from pathlib import Path

from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.models import Wine
from app.core.database import Base

ROOT = Path(__file__).resolve().parent.parent
WEBSITE_DATA = ROOT / "website" / "src" / "data"


def strip_comments(s: str) -> str:
    # remove // line comments and /* */ blocks
    s = re.sub(r"^\s*//.*$", "", s, flags=re.MULTILINE)
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.DOTALL)
    return s


def extract_array(ts: str) -> str:
    # get the first [ ... ] block after '='
    m = re.search(r"=\s*\[", ts)
    if not m:
        raise ValueError("No array start found")
    start = m.end() - 1
    # find matching closing bracket by counting
    depth = 0
    end = None
    for i in range(start, len(ts)):
        c = ts[i]
        if c == '[':
            depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    if end is None:
        raise ValueError("No closing bracket for array")
    return ts[start:end]


def ts_array_to_json(array_src: str) -> str:
    s = array_src
    # replace single quotes with double quotes first (string content)
    s = re.sub(r"'", '"', s)
    # quote unquoted keys before ':' not preceded by a quote
    s = re.sub(r"(?<!\")([A-Za-z_][A-Za-z0-9_]*)\s*:\s", r'"\1": ', s)
    # remove trailing commas before } or ]
    s = re.sub(r",\s*([}\]])", r"\1", s)
    return s


def load_wines_from_ts() -> list[dict]:
    wines = []
    for fname in ["tintos.ts", "blancos.ts", "rosados.ts"]:
        path = WEBSITE_DATA / fname
        if not path.exists():
            continue
        raw = path.read_text(encoding="utf-8")
        raw = strip_comments(raw)
        array_src = extract_array(raw)
        json_like = ts_array_to_json(array_src)
        try:
            data = json.loads(json_like)
        except Exception as e:
            raise RuntimeError(f"Failed to parse {fname}: {e}")
        for item in data:
            # normalize fields and coerce types
            wine = {
                "id": str(item.get("id")),
                "name": item.get("name") or "",
                "color": item.get("color"),
                "grape": item.get("grape") or "",
                "origin": item.get("origin"),
                "short_description": item.get("shortDescription"),
                "long_description": item.get("longDescription"),
                "image": item.get("image"),
                "characteristics": item.get("characteristics"),
                "available": bool(item.get("available", True)),
                "prices": item.get("prices") or {},
            }
            wines.append(wine)
    return wines


def sync_db(wines: list[dict]):
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        # Clear
        session.query(Wine).delete()
        session.commit()
        # Insert
        for w in wines:
            session.add(Wine(**w))
        session.commit()
        print(f"Synced {len(wines)} wines from TS data")
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    wines = load_wines_from_ts()
    sync_db(wines)
