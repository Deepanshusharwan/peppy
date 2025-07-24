from collections.abc import Callable
from typing import Any


def find_ordered_subsequence(query: str, target: str) -> list[int] | None:
    """
    Find the ordered subsequence of the query string in the target string.

    If found, returns a list of indices in the target string where each character
    in the query string appears in order.
    If the sequence is not found in order, returns None.
    """
    indices = []
    # Starting position for search in the target string
    current_pos_in_target = 0

    for char_in_query in query:
        # Search for the current character starting from the last found position
        found_at = target.find(char_in_query, current_pos_in_target)

        # If not found, return None to indicate failed match
        if found_at == -1:
            return None

        # Record the found index and update the starting position for the next search
        indices.append(found_at)
        current_pos_in_target = found_at + 1

    return indices


def search_by_subsequence[T: Any](
    query: str, items: list[T], key: Callable[[T], str] | None = None
) -> list[dict]:
    """
    Filter and score items based on ordered subsequence matching.

    - Filters out items that do not contain all query characters in order.
    - Matches are scored and ranked:
        The earlier the match starts and the shorter the character span, the higher the rank.
    """
    results = []

    for item in items:
        item_str = key(item) if key else item

        # Find the ordered subsequence indices
        indices = find_ordered_subsequence(query, item_str)

        # If indices are returned, the match is successful
        if indices:
            # Calculate the match score
            start_position = indices[0]
            # Span is the total gap between matched characters
            span = indices[-1] - indices[0] - (len(indices) - 1)

            score = start_position * 2 + span
            score = max(100 - score, 1)

            results.append({"item": item, "score": score})

    return results


def search_and_sort_apps[T: Any](
    query: str, apps: list[T], key: Callable[[T], str], open_count: Callable[[T], int]
) -> list[T]:
    """
    Search and sort applications by fuzzy query and open count.

    This function first filters and scores apps using ordered subsequence matching (see search_by_subsequence).
    Then, it boosts the score based on each app's open count.

    Score formula:
        base_score = 100 - (start_position * 2 + span)
        final_score = base_score * (open_count / max_open_count + 1)

    Args:
        query: The search string.
        apps: List of app objects.
        key: Function to extract string from app.
        open_count: Function to get open count for each app.

    Returns:
        List of apps sorted by final score (descending).
    """
    # Get fuzzy match results with base score
    if query:
        results = search_by_subsequence(query, apps, key)
    else:
        results = [{"item": i, "score": 100} for i in apps]

    # Find the maximum open count for normalization
    max_open_count = 1
    for i in results:
        max_open_count = max(max_open_count, open_count(i["item"]))

    for i in results:
        # Boost score by open count
        i["score"] = i["score"] * (open_count(i["item"]) / max_open_count + 1)
        #print(key(i["item"]), i["score"])

    results.sort(key=lambda x: x["score"], reverse=True)
    return [i["item"] for i in results]
