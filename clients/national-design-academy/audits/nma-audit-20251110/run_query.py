#!/usr/bin/env python3
"""Execute GAQL query against Google Ads API"""
import sys
import json
from google.ads.googleads.client import GoogleAdsClient
from google.protobuf.json_format import MessageToDict

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 run_query.py <customer_id> [query_file]")
        sys.exit(1)

    customer_id = sys.argv[1]

    # Read query from file or stdin
    if len(sys.argv) > 2:
        with open(sys.argv[2], 'r') as f:
            query = f.read().strip()
    else:
        query = sys.stdin.read().strip()

    # Load client
    client = GoogleAdsClient.load_from_storage('/Users/administrator/google-ads.yaml')
    ga_service = client.get_service('GoogleAdsService')

    # Execute query
    try:
        response = ga_service.search(customer_id=customer_id, query=query)

        results = []
        for row in response:
            # Convert protobuf to dict
            row_dict = MessageToDict(row._pb, preserving_proto_field_name=True)
            results.append(row_dict)

        print(json.dumps(results, indent=2))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
