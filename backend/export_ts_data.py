import json
import re
from pathlib import Path

def parse_ts_wine_data(file_path):
    """Parse TypeScript wine data files into Python dicts"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    wines = []
    
    wine_blocks = re.findall(r'\{[^\{]*?name:[^\{]*?prices:[^\{]*?\{[^\}]*?\}[^\}]*?\}', content, re.DOTALL)
    
    for block in wine_blocks:
        try:
            wine = {}
            
            name_match = re.search(r'name:\s*[\'"]([^\'"]+)[\'"]', block)
            if name_match:
                wine['name'] = name_match.group(1)
            
            id_match = re.search(r'id:\s*[\'"]?([^\'"،\s]+)[\'"]?', block)
            if id_match:
                wine['id'] = str(id_match.group(1))
            
            prices_match = re.search(r'prices:\s*\{([^}]+)\}', block)
            if prices_match:
                prices_str = prices_match.group(1)
                prices = {}
                price_items = re.findall(r'[\'"]?([^\'":\s,]+)[\'"]?\s*:\s*[\'"]([^\'"]+)[\'"]', prices_str)
                for key, value in price_items:
                    if key and value:
                        prices[key] = value
                wine['prices'] = prices
            
            color_match = re.search(r'color:\s*[\'"]([^\'"]+)[\'"]', block)
            if color_match:
                wine['color'] = color_match.group(1)
            
            grape_match = re.search(r'grape:\s*[\'"]([^\'"]+)[\'"]', block)
            if grape_match:
                wine['grape'] = grape_match.group(1)
            
            origin_match = re.search(r'origin:\s*[\'"]([^\'"]+)[\'"]', block)
            if origin_match:
                wine['origin'] = origin_match.group(1)
            
            short_match = re.search(r'shortDescription:\s*[\'"]([^\'"]+)[\'"]', block, re.DOTALL)
            if short_match:
                wine['short_description'] = short_match.group(1)
            
            long_match = re.search(r'longDescription:\s*[\'"]([^\'"]+)[\'"]', block, re.DOTALL)
            if long_match:
                wine['long_description'] = long_match.group(1)
            
            char_match = re.search(r'characteristics:\s*[\'"]([^\'"]+)[\'"]', block)
            if char_match:
                wine['characteristics'] = char_match.group(1)
            
            avail_match = re.search(r'available:\s*(true|false)', block)
            wine['available'] = avail_match.group(1) == 'true' if avail_match else True
            
            wine['image'] = None
            
            if 'name' in wine:
                wines.append(wine)
                
        except Exception as e:
            print(f"Error parsing wine block: {e}")
            continue
    
    return wines

def main():
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'data'
    output_dir = project_root / 'backend' / 'data'
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    all_wines = []
    
    for file_name in ['tintos.ts', 'blancos.ts', 'rosados.ts']:
        file_path = data_dir / file_name
        if file_path.exists():
            wines = parse_ts_wine_data(file_path)
            all_wines.extend(wines)
            print(f"Parsed {len(wines)} wines from {file_name}")
    
    output_file = output_dir / 'wines.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_wines, f, indent=2, ensure_ascii=False)
    
    print(f"\nTotal: Exported {len(all_wines)} wines to {output_file}")

if __name__ == '__main__':
    main()
