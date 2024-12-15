class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self._title = title  
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        if hasattr(self, "_title"):  
            raise AttributeError("Title cannot be changed")
        if isinstance(new_title, str):
            if 5 <= len(new_title) <= 50:
                self._title = new_title
            else:
                raise ValueError("Title must be between 5 and 50 characters")
        else:
            raise TypeError("Title must be a string")

    def __repr__(self):
        return f'<Article {self.title}>'

    
    def get_article_by_id(article_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM Article WHERE id = ?
        ''', (article_id,))
        article_row = cursor.fetchone()
        conn.close()
        if article_row:
            author = Author.get_author_by_id(article_row['author_id'])
            magazine = Magazine.get_magazine_by_id(article_row['magazine_id'])
            return Article(article_row['id'], article_row['title'], article_row['content'], author.id, magazine.id)
        return None

    def update_content(self, new_content):
        self.content = new_content
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Article SET content = ? WHERE id = ?
        ''', (self.content, self.id))
        conn.commit()
        conn.close()

    
    def delete_article(article_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM Article WHERE id = ?
        ''', (article_id,))
        conn.commit()
        conn.close()
