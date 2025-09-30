import sys
sys.path.append('.')

from app.core.database import SessionLocal
from app.models.wine import Wine

session = SessionLocal()
wines = session.query(Wine).all()

print(f'Total wines in database: {len(wines)}')
print('\nWines by color:')

colors = {}
for wine in wines:
    if wine.color not in colors:
        colors[wine.color] = []
    colors[wine.color].append(wine.name)

for color, wine_names in colors.items():
    print(f'\n{color.upper()}:')
    for name in wine_names:
        print(f'  - {name}')

session.close()