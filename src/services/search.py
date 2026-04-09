def search_books(query, books):
    """
    Пошук книг за назвою або автором
    :param query: рядок пошуку
    :param books: список словників з книгами
    :return: список знайдених книг
    """
    results = []

    for book in books:
        if query.lower() in book["title"].lower() or query.lower() in book["author"].lower():
            results.append(book)

    return results