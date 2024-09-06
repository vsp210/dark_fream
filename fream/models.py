import sqlite3
from abc import ABC, abstractmethod

class Field(ABC):
    """
    Base class for all field types.
    """

    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name', None)
        self.verbose_name = kwargs.pop('verbose_name', None)
        self.primary_key = kwargs.pop('primary_key', False)
        self.unique = kwargs.pop('unique', False)
        self.default = kwargs.pop('default', None)
        self.null = kwargs.pop('null', False)
        self.blank = kwargs.pop('blank', False)
        self.editable = kwargs.pop('editable', True)
        self.db_index = kwargs.pop('db_index', False)

    @abstractmethod
    def get_internal_type(self):
        pass

    @abstractmethod
    def to_python(self, value):
        pass

    @abstractmethod
    def get_prep_value(self, value):
        pass

    @abstractmethod
    def contribute_to_class(self, cls, name):
        pass

    def deconstruct(self):
        """
        Returns a tuple of four elements:
        - the class name of the field
        - the arguments to the constructor
        - the keyword arguments to the constructor
        - the name of the field in the model
        """
        args = tuple()
        kwargs = {k: v for k, v in self.__dict__.items() if k not in ('name', 'attname')}
        return (self.__class__.__name__, args, kwargs, self.name)

class CharField(Field):
    """
    Field for storing strings.
    """

    def __init__(self, max_length=None, *args, **kwargs):
        self.max_length = max_length
        kwargs['verbose_name'] = kwargs.get('verbose_name', 'CharField')
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'CharField'

    def to_python(self, value):
        if isinstance(value, str):
            return value
        return str

class TextField(Field):
    """
    Field for storing text.
    """

    def __init__(self, max_length=None, *args, **kwargs):
        self.max_length = max_length
        kwargs['verbose_name'] = kwargs.get('verbose_name', 'TextField')
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'TextField'

    def to_python(self, value):
        if isinstance(value, str):
            return value
        return str

class IntegerField(Field):
    """
    Field for storing integers.
    """

    def __init__(self, *args, **kwargs):
        kwargs['verbose_name'] = kwargs.get('verbose_name', 'IntegerField')
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'IntegerField'

    def to_python(self, value):
        if isinstance(value, int):
            return value
        return int

class ImageField(Field):
    """
    Field for storing images.
    """

    def __init__(self, upload_to='', *args, **kwargs):
        self.upload_to = upload_to
        kwargs['verbose_name'] = kwargs.get('verbose_name', 'ImageField')
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'ImageField'

    def to_python(self, value):
        if isinstance(value, bytes):
            return value
        return bytes

class DateField(Field):
    """
    Field for storing dates.
    """

    def __init__(self, *args, **kwargs):
        kwargs['verbose_name'] = kwargs.get('verbose_name', 'DateField')
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'DateField'

    def to_python(self, value):
        if isinstance(value, str):
            return value
        return str

class BooleanField(Field):
    """
    Field for storing boolean values.
    """

    def __init__(self, *args, **kwargs):
        kwargs['verbose_name'] = kwargs.get('verbose_name', 'BooleanField')
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'BooleanField'

    def to_python(self, value):
        if isinstance(value, bool):
            return value
        return bool

class ForeignKey(Field):
    """
    Field for storing foreign keys.
    """

    def __init__(self, model, *args, **kwargs):
        self.model = model
        kwargs['verbose_name'] = kwargs.get('verbose_name', 'ForeignKey')
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'ForeignKey'

    def to_python(self, value):
        if isinstance(value, int):
            return value
        return int

class FloatField(Field):
    """
    Field for storing floating point numbers.

    Args:
        verbose_name (str, optional): The verbose name of the field. Defaults to None.

    Returns:
        FloatField: The FloatField instance.

    Example:
        FloatField(verbose_name='price')
    """
    def __init__(self, verbose_name=None):
        super().__init__('REAL', verbose_name)

class ManyToManyField(Field):
    """
    Field for storing many-to-many relationships.

    Args:
        model (Model): The model that the many-to-many field references.
        verbose_name (str, optional): The verbose name of the field. Defaults to None.

    Returns:
        ManyToManyField: The ManyToManyField instance.

    Example:
        ManyToManyField(Tag, verbose_name='tags')
    """
    def __init__(self, model, verbose_name=None):
        super().__init__('INTEGER', verbose_name)
        self.model = model


class ModelMeta(type):
    """
    Metaclass for Model.

    This metaclass is used to automatically collect fields from the Model class.
    """
    def __new__(meta, name, bases, attrs):
        fields = {}
        for key, value in attrs.items():
            if isinstance(value, Field):
                fields[key] = value
        attrs['_fields'] = fields
        return type.__new__(meta, name, bases, attrs)


class Model(metaclass=ModelMeta):
    """
    Base class for all models.

    This class provides methods for interacting with the database.

    Attributes:
        _fields (dict): A dictionary of fields in the model.

    Example:
        >>> class User(Model):
        ...     id = Field('INTEGER', 'ID')
        ...     name = Field('TEXT', 'Name')
        ...     age = Field('INTEGER', 'Age')
        ...
        >>> User.create_table()
        >>> user = User(id=1, name='John Doe', age=30)
        >>> user.save()
        >>> User.get(id=1)
        User(id=1, name='John Doe', age=30)
    """

    def __init__(self, **kwargs):
        """
        Initialize the model instance.

        Args:
            **kwargs: Keyword arguments for the model fields.
        """
        self.__dict__.update(kwargs)

    @classmethod
    def get_fields(cls):
        """
        Get the fields of the model.

        Returns:
            list: A list of tuples containing the field name and type.
        """
        return [(field_name, field_type) for field_name, field_type in cls._fields.items()]

    @classmethod
    def get(cls, **param):
        """
        Get a model instance from the database.

        Args:
            **param: Keyword arguments for the model fields to filter by.

        Returns:
            Model: The model instance if found, otherwise None.
        """
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
        """
        Get all model instances from the database.

        Returns:
            list: A list of model instances.
        """
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        sql = f'SELECT * FROM [{cls.__name__}]'
        cursor.execute(sql)
        results = cursor.fetchall()
        conn.close()
        return [cls(**dict(zip([field_name for field_name, _ in cls.get_fields()], result))) for result in results]

    @classmethod
    def get_db_connection(cls):
        """
        Get a connection to the database.

        Returns:
            sqlite3.Connection: The database connection.
        """
        return sqlite3.connect('db.db')

    def save(self):
        """
        Save the model instance to the database.
        """
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(self.get_insert_sql(), self.get_values())
        conn.commit()
        conn.close()

    def get_insert_sql(self):
        """
        Get the SQL query to insert the model instance into the database.

        Returns:
            str: The SQL query.
        """
        fields = [field_name for field_name, _ in self.get_fields()]
        table_name = f'[{self.__class__.__name__}]'
        sql = f'INSERT INTO {table_name} ({", ".join(fields)}) VALUES ({", ".join(["?"] * len(fields))})'
        return sql

    def get_values(self):
        """
        Get the values to insert into the database.

        Returns:
            list: A list of values.
        """
        return [getattr(self, field_name) for field_name, _ in self._fields.items()]

    def get_verbose_names(self):
        """
        Get a dictionary of verbose names for the model fields.

        Returns:
            dict: A dictionary where the keys are the field names and the values are the verbose names.

        Example:
            >>> user = User(id=1, name='John Doe', age=30)
            >>> user.get_verbose_names()
            {'id': 'ID', 'name': 'Name', 'age': 'Age'}
        """
        return {field_name: field_type.verbose_name for field_name, field_type in self._fields.items()}


    @classmethod
    def create_table(cls):
        """
        Create the database table for the model.

        This method creates the table in the database if it does not already exist.
        """
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(cls.get_create_table_sql())
        conn.commit()
        conn.close()


    @classmethod
    def get_create_table_sql(cls):
        """
        Get the SQL query to create the database table for the model.

        Returns:
            str: The SQL query to create the table.

        Example:
            >>> User.get_create_table_sql()
            'CREATE TABLE IF NOT EXISTS [User] (id INTEGER, name TEXT, age INTEGER)'
        """
        fields = [(field_name, field_type.field_type) for field_name, field_type in cls._fields.items()]
        table_name = f'[{cls.__name__}]'
        sql = f'CREATE TABLE IF NOT EXISTS {table_name} ('
        sql += ', '.join(f'{field_name} {field_type}' for field_name, field_type in fields)
        sql += ')'
        return sql
