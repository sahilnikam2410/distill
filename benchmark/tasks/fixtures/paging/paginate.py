def page_bounds(page, size):
    """Slice bounds for a 1-based page number."""
    start = (page - 1) * size
    return start, start + size


def paginate(items, page, size):
    start, end = page_bounds(page, size)
    return items[start:end]
