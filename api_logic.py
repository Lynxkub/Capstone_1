import requests, json

def get_product_id(api_results):
    results = json.dumps(api_results.json())
    starting_point = results.find('item_id')
    item_info = results[starting_point : (starting_point + 30)]
    list_of_nums = []
    for el in item_info:
        try:
            list_of_nums.append(int(el))
        except ValueError:
            pass
    s = [str(i) for i in list_of_nums]
    res = int("".join(s))
    return res

def get_product_price(api_results):
    results = json.dumps(api_results.json())
    starting_point = results.find('price')
    item_info = results[starting_point : (starting_point + 15)]
    list_of_nums = []
    for el in item_info:
        try:
            list_of_nums.append(int(el))
        except ValueError:
            pass
    s = [str(i) for i in list_of_nums]
    res = int("".join(s))
    return res

def make_api_search(search_term):
    params = {
    'api_key': 'AA64FA32C802407CB60FC92CA4A08418',
    'type': 'search',
    'search_term': search_term,
    'customer_zipcode': '53220'
}
    api_result = requests.get('https://api.bluecartapi.com/request', params)
    return api_result

def specific_product_search(item_id):
    params = {
  'api_key': 'AA64FA32C802407CB60FC92CA4A08418',
  'type': 'product',
  'item_id': item_id
}
    api_result = requests.get('https://api.bluecartapi.com/request', params)
    return api_result

def product_api_search(search_term):
    first_call = make_api_search(search_term)
    item_id = get_product_id(first_call)
    item_details = specific_product_search(item_id)
    item_price = get_product_price(item_details)
    return (search_term, (item_price / 100))