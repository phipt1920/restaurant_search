import pandas as pd
from elasticsearch.exceptions import RequestError
from elastic_utils import get_es_client, create_index, INDEX_NAME

def load_data(es):
    df = pd.read_csv("data/sample_restaurants.csv")

    for _, row in df.iterrows():
        try:
            lat_str, lon_str = row["location"].split(",")
            lat = float(lat_str.strip())
            lon = float(lon_str.strip())
            
            doc = {
                "restaurant_id": row["restaurant_id"],
                "restaurant_name": row["restaurant_name"],
                "description": row["description"],
                "location": {
                    "lat": lat,
                    "lon": lon
                },
                "cuisine_type": row["cuisine_type"],
                "rating": float(row["rating"])
            }
            es.index(index=INDEX_NAME, id=str(row["restaurant_id"]), document=doc)
        except Exception as e:
            print(f"Error indexing row {row['restaurant_id']}: {e}")

    print("✅ Data loaded successfully.")

if __name__ == "__main__":
    es = get_es_client()
    try:
        create_index(es)
        print("Index created.")
    except RequestError as e:
        if "resource_already_exists_exception" in str(e):
            print("Index already exists. Skipping index creation.")
        else:
            raise

    load_data(es)
