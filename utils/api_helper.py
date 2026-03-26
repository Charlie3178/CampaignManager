import requests

BASE_URL = "https://www.dnd5eapi.co"


def fetch_srd(endpoint):
    """
    Fetches data from the SRD API. 
    Handles pagination automatically if the endpoint returns multiple pages.
    """
    all_results = []
    # Ensure the endpoint starts with /api/
    current_url = f"{BASE_URL}/api/{endpoint.replace('/api/', '')}"

    while current_url:
        try:
            response = requests.get(current_url)
            response.raise_for_status()
            data = response.json()

            # If this is a list endpoint (has 'results')
            if 'results' in data:
                all_results.extend(data['results'])

                # Check for next page
                next_page = data.get('next')
                current_url = f"{BASE_URL}{next_page}" if next_page else None
            else:
                # This is a single detail endpoint (no pagination needed)
                return data

        except Exception as e:
            print(f"Error fetching {current_url}: {e}")
            break

    return {'results': all_results}
