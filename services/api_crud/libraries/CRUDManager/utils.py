# Standard Library
# * wraps es un decorador que se usa para actualizar la función wrapper
# * con los atributos de la función original
from functools import wraps
import asyncio


def take_first_pair(dictionary: dict) -> tuple:
    """
    Obtiene el primer par clave-valor de un diccionario.

    Args:
        dictionary (dict): El diccionario del cual obtener el primer par clave-valor.

    Returns:
        tuple: El primer par clave-valor del diccionario en forma de tupla (clave, valor).
    """
    return next(iter(dictionary.items()))


def adapt_value_for_sql(value: str | int) -> str:
    """
    Prepara un valor para ser incluido en una sentencia SQL.

    Esta función toma un valor que puede ser de tipo entero o cadena de texto (string).
    Si el valor es un entero, lo convierte a una cadena de texto. Si el valor es una
    cadena de texto, añade comillas simples alrededor del valor para que pueda ser
    insertado en una sentencia SQL como un valor de cadena.

    Args:
        value (str | int): El valor que se va a adaptar para la sentencia SQL.

    Returns:
        str: El valor adaptado como una cadena de texto lista para ser insertada en SQL.
    """
    if type(value) == int:
        return str(value)
    elif type(value) == str:
        return f"'{value}'"
    else:
        raise ValueError("The value must be a text string or an integer.")


def ensure_kwargs_count(func, allowed_kwarg_count: int = 1):
    """
    Decorador para asegurar que una función asíncrona reciba una cantidad
    específica de argumentos de palabra clave.

    Args:
    - `func (callable)`: Función asíncrona a decorar.

    - `allowed_kwarg_count (int, optional)`: Número permitido de kwargs
    que la función debería recibir. valor por defecto `1`.

    Raises:
        TypeError: Si la función a decorar no es asíncrona.
        TypeError: Si supera la cantidad de argumentos de palabra clave.

    Returns:
        func (callable): Función decorada.
    """
    if not asyncio.iscoroutinefunction(func):
        raise TypeError(
            "The 'ensure_kwargs_count' decorator can only be applied to asynchronous functions."
        )

    @wraps(func)
    async def wrapper(*args, **kwargs):
        if len(kwargs) != allowed_kwarg_count:
            raise TypeError(f"{func.__name__} expects exactly one keyword argument")
        else:
            return await func(*args, **kwargs)

    return wrapper
