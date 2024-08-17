import sqlite3

class Field:
    def __init__(self, field_type):
        self.field_type = field_type

    def __repr__(self):
        return f'Field({self.field_type})'


class CharField(Field): # Строка
    def __init__(self, max_length=255):
        super().__init__('TEXT')
        self.max_length = max_length


class TextField(Field): # Текст
    def __init__(self, max_length=1024):
        super().__init__('TEXT')
        self.max_length = max_length


class IntegerField(Field): # Числа
    def __init__(self):
        super().__init__('INTEGER')


class ImageField(Field):  # Картинка
    def __init__(self, upload_to=''):
        super().__init__('BLOB')
        self.upload_to = upload_to

    def __repr__(self):
        return f'ImageField(upload_to={self.upload_to})'


class ModelMeta(type):
    def __new__(meta, name, bases, attrs):
        fields = {}
        for key, value in attrs.items():
            if isinstance(value, Field):
                fields[key] = value
        attrs['_fields'] = fields
        return type.__new__(meta, name, bases, attrs)


class Model(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @classmethod
    def get_fields(self):
        return [(field_name, field_type) for field_name, field_type in self._fields.items()]

    @classmethod
    def get(cls, **param):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        fields = [(field_name, field_type) for field_name, field_type in cls.get_fields() if field_name in param]
        where_clause = ' AND '.join([f"{field_name} = ?" for field_name, _ in fields])
        sql = f'SELECT * FROM [{cls.__name__}] WHERE {where_clause}'
        cursor.execute(sql, tuple(param[field_name] for field_name, _ in fields))
        result = cursor.fetchone()
        conn.close()
        if result:
            return cls(**dict(zip([field_name for field_name, _ in cls.get_fields()], result)))
        else:
            return None

    @classmethod
    def all(cls):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        sql = f'SELECT * FROM [{cls.__name__}]'
        cursor.execute(sql)
        results = cursor.fetchall()
        conn.close()
        return [cls(**dict(zip([field_name for field_name, _ in cls.get_fields()], result))) for result in results]

    @classmethod
    def get_db_connection(cls):
        return sqlite3.connect('db.db')

    def save(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(self.get_insert_sql(), self.get_values())
        conn.commit()
        conn.close()

    def get_insert_sql(self):
        fields = [field_name for field_name, _ in self.get_fields()]
        table_name = f'[{self.__class__.__name__}]'
        sql = f'INSERT INTO {table_name} ({", ".join(fields)}) VALUES ({", ".join(["?"] * len(fields))})'
        return sql

    def get_values(self):
        return [getattr(self, field_name) for field_name, _ in self._fields.items()]

    def create_table(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(self.get_create_table_sql())
        conn.commit()
        conn.close()

    def get_create_table_sql(self):
        fields = [(field_name, field_type.field_type) for field_name, field_type in self._fields.items()]
        table_name = f'[{self.__class__.__name__}]'
        sql = f'CREATE TABLE IF NOT EXISTS {table_name} ('
        sql += ', '.join(f'{field_name} {field_type}' for field_name, field_type in fields)
        sql += ')'
        return sql