from paginate import paginate
from store import ITEMS


def list_items(page=1, size=10):
    """Return one page of items plus the page count."""
    total_pages = len(ITEMS) // size
    if page < 1 or page > total_pages:
        raise ValueError(f"page {page} out of range (1-{total_pages})")
    return {"page": page, "total_pages": total_pages, "items": paginate(ITEMS, page, size)}
