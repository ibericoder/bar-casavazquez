import json
from pathlib import Path
from sqlalchemy.orm import sessionmaker
from app.core.database import engine, Base
from app.models import Wine

HERE = Path(__file__).parent
DATA = HERE / 'wines_from_ts.json'

def main():
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    s = Session()
    try:
        raw = json.loads(DATA.read_text(encoding='utf-8'))
        # Deduplicate by id, prefer available=True if duplicates
        by_id = {}
        for w in raw:
            wid = str(w.get('id'))
            if wid in by_id:
                existing = by_id[wid]
                take_current = (w.get('available', True) and not existing.get('available', True)) or True
                if take_current:
                    by_id[wid] = w
            else:
                by_id[wid] = w
        data = list(by_id.values())
        s.query(Wine).delete()
        s.commit()
        for w in data:
            s.add(Wine(**w))
        s.commit()
        print(f'Loaded {len(data)} wines into DB')
    finally:
        s.close()

if __name__ == '__main__':
    main()
