class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        if isinstance(id, int):
            self._id = id
        else:
            raise ValueError("ID must be an integer")
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name):
        if hasattr(self, "name"):
            AttributeError("Name cannot be changed")
        else:
            if isinstance(new_name, str):
                if len(new_name) > 0:
                    self._name = new_name
                else:
                    ValueError("Name must be longer than 0 characters")
            else:
                TypeError("Name must be a string")

    def __repr__(self):
        return f'<Author {self.name}>'

    
    def get_author_by_id(author_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM Author WHERE id = ?
        ''', (author_id,))
        author_row = cursor.fetchone()
        conn.close()
        if author_row:
            return Author(author_row['id'], author_row['name'])
        return None

    def update_name(self, new_name):
        self.name = new_name
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Author SET name = ? WHERE id = ?
        ''', (self.name, self.id))
        conn.commit()
        conn.close()

    
    def delete_author(author_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM Author WHERE id = ?
        ''', (author_id,))
        conn.commit()
        conn.close()

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM Article WHERE author_id = ?
        ''', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return articles

    def magazines(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT Magazine.* FROM Magazine
            JOIN Article ON Magazine.id = Article.magazine_id
            WHERE Article.author_id = ?
        ''', (self.id,))
        magazines = cursor.fetchall()
        conn.close()
        return magazines