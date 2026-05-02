from extract import extract_all
from transform import transform
from dimensions import load_dimensions, load_static_dimensions
from lookups import build_lookups
from facts import build_facts

def run_pipeline():
    data = extract_all()
    data = transform(data)

    load_dimensions(data)
    
    load_static_dimensions(data)

    lookups = build_lookups()

    build_facts(data, lookups)

    print(" FULL ETL Pipeline Completed Successfully")

if __name__ == "__main__":
    run_pipeline()