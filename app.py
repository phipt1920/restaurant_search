from flask import Flask, request, jsonify
from elastic_utils import get_es_client, INDEX_NAME

app = Flask(__name__)
es = get_es_client()

@app.route("/search")
def search():
    query = request.args.get("query", "").strip()

    if query:
        es_query = {
            "multi_match": {
                "query": query,
                "fields": ["restaurant_name", "description"],
                "fuzziness": "AUTO"
            }
        }
    else:
        es_query = {
            "match_all": {}
        }

    response = es.search(index=INDEX_NAME, body={"query": es_query})
    hits = response["hits"]["hits"]
    return jsonify([hit["_source"] for hit in hits])


@app.route("/nearby")
def nearby():
    query = request.args.get("query", "").strip()
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error": "Missing lat or lon"}), 400

    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return jsonify({"error": "Invalid lat or lon format"}), 400

    must_clause = []
    if query:
        must_clause.append({
            "multi_match": {
                "query": query,
                "fields": ["restaurant_name", "description"],
                "fuzziness": "AUTO"
            }
        })

    body = {
        "query": {
            "bool": {
                "must": must_clause if must_clause else {"match_all": {}},
                "filter": {
                    "geo_distance": {
                        "distance": "5km",
                        "location": {
                            "lat": lat,
                            "lon": lon
                        }
                    }
                }
            }
        },
        "sort": [
            {
                "_geo_distance": {
                    "location": {"lat": lat, "lon": lon},
                    "order": "asc",
                    "unit": "km"
                }
            }
        ]
    }

    # Debug: in ra body để kiểm tra trước khi gọi ES
    print("ES query body:", body)

    res = es.search(index=INDEX_NAME, body=body)
    hits = res["hits"]["hits"]
    return jsonify([hit["_source"] for hit in hits])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
