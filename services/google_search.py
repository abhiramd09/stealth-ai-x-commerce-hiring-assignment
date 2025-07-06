from googlesearch import search

QUERY = "Buy {queryProduct} in {queryCountry}"
MAXIMUM_NUMBER_OF_RESULTS = 6

def get_search_query_urls(
        query_product: str, query_country: str, num_results: int = MAXIMUM_NUMBER_OF_RESULTS) -> list[str]:
    """
    Perform a Google search and return a list of URLs.

    :param query_product: The product searched.
    :param query_country: The country where the product is searched.
    :param num_results: The maximum number of results to return.
    :return: A list of URLs from the search results.
    """
    query = QUERY.format(queryProduct=query_product, queryCountry=query_country)
    return [url for url in search(query, num_results=num_results)]

