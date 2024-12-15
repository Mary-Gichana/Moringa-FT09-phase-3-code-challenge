class Magazine:
    def __init__(self, id, name, category="General"):
        self.id = id
        self.name = name
        self.category = category

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id

    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name):
        if isinstance(new_name, str):
            if len(new_name) >= 2 and len(new_name) <= 16:
                self._name = new_name
            else:
                ValueError("Name must be between 2 and 16 characters")
        else:
            TypeError("Name must be a string")

    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, new_category):
        if isinstance(new_category, str):
            if len(new_category) > 0:
                self._category = new_category
            else:
                ValueError("Category must have at least one character")
        else:
            TypeError("Category must be a string")
        

    def __repr__(self):
        return f'<Magazine {self.name}>'

    
    def get_magazine_by_id(magazine_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM Magazine WHERE id = ?
        ''', (magazine_id,))
        magazine_row = cursor.fetchone()
        conn.close()
        if magazine_row:
            return Magazine(magazine_row['id'], magazine_row['name'], magazine_row['category'])
        return None

    def update_magazine(self, new_name, new_category):
        self.name = new_name
        self.category = new_category
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Magazine SET name = ?, category = ? WHERE id = ?
        ''', (self.name, self.category, self.id))
        conn.commit()
        conn.close()

    
    def delete_magazine(magazine_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM Magazine WHERE id = ?
        ''', (magazine_id,))
        conn.commit()
        conn.close()

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM Article WHERE magazine_id = ?
        ''', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return articles

    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT Author.* FROM Author
            JOIN Article ON Author.id = Article.author_id
            WHERE Article.magazine_id = ?
        ''', (self.id,))
        contributors = cursor.fetchall()
        conn.close()
        return contributors

    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT title FROM Article WHERE magazine_id = ?
        ''', (self.id,))
        titles = [row['title'] for row in cursor.fetchall()]
        conn.close()
        return titles if titles else None

    def contributing_authors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT Author.*, COUNT(Article.id) as article_count FROM Author
            JOIN Article ON Author.id = Article.author_id
            WHERE Article.magazine_id = ?
            GROUP BY Author.id
            HAVING article_count > 2
        ''', (self.id,))
        authors = [Author(row['id'], row['name']) for row in cursor.fetchall()]
        conn.close()
        return authors if authors else None