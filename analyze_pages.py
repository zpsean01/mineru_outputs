import json
import os
import glob

base_dir = r"C:\Users\Admin\MinerU"
# Find all matching directories
dirs = sorted(glob.glob(os.path.join(base_dir, "NCB-PCI_Express_Base_6.0.pdf-*")))

results = []
for d in dirs:
    dirname = os.path.basename(d)
    # Find content_list_v2.json files
    json_files = glob.glob(os.path.join(d, "*_content_list_v2.json"))
    if not json_files:
        print(f"{dirname}: No content_list_v2.json found")
        continue
    
    json_file = json_files[0]
    filename = os.path.basename(json_file)
    
    # Read the JSON
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # data is a list of pages
    if isinstance(data, list) and len(data) > 0:
        # Each page has page_idx or page_number
        page_indices = []
        for page in data:
            if isinstance(page, dict):
                if "page_idx" in page:
                    page_indices.append(page["page_idx"])
                elif "page_number" in page:
                    page_indices.append(page["page_number"])
            elif isinstance(page, list):
                # In some formats, it might be nested
                pass
        
        if page_indices:
            min_page = min(page_indices)
            max_page = max(page_indices)
            total_pages = len(data)
            total_items = len(page_indices)
            
            # Check for config.json
            config_file = os.path.join(d, "config.json")
            config_content = None
            if os.path.exists(config_file):
                with open(config_file, "r", encoding="utf-8") as f:
                    config_content = f.read()
            
            # Also check for layout.json which might have metadata
            layout_file = os.path.join(d, "layout.json")
            layout_content = None
            if os.path.exists(layout_file):
                with open(layout_file, "r", encoding="utf-8") as f:
                    layout_content = f.read()[:500]  # first 500 chars
            
            results.append({
                "dirname": dirname,
                "filename": filename,
                "min_page_idx": min_page,
                "max_page_idx": max_page,
                "total_pages": total_pages,
                "config_json": config_content,
                "layout_json": layout_content,
                "sample_first_page": data[0] if data else None,
                "sample_last_page": data[-1] if data else None,
            })
        else:
            # The JSON might have a different structure
            # Print the structure
            sample = str(data)[:500]
            print(f"{dirname}: No page_idx found. Structure: {sample}")
    else:
        print(f"{dirname}: Empty or non-list data")

# Print summary table
print("\n" + "="*180)
print(f"{'Directory Name':<65} {'Filename':<50} {'Min Page':<10} {'Max Page':<10} {'Total Pages':<12}")
print("="*180)
for r in results:
    print(f"{r['dirname']:<65} {r['filename']:<50} {r['min_page_idx']:<10} {r['max_page_idx']:<10} {r['total_pages']:<12}")
print("="*180)

# Print config.json for each
print("\n\n=== Config JSON contents ===")
for r in results:
    print(f"\n--- {r['dirname']} ---")
    if r['config_json']:
        print(r['config_json'])
    else:
        print("No config.json found")
    
    print(f"\nLayout.json (first 500 chars):")
    if r['layout_json']:
        print(r['layout_json'])
    else:
        print("No layout.json found or empty")
        
    print(f"\nFirst page sample keys: {list(r['sample_first_page'].keys()) if isinstance(r['sample_first_page'], dict) else 'not a dict'}")
    print(f"Last page sample keys: {list(r['sample_last_page'].keys()) if isinstance(r['sample_last_page'], dict) else 'not a dict'}")