"""
DAO = Data Access Object.
Es un componente de software que suministra una interfaz común entre la aplicación y
uno o más dispositivos de almacenamiento de datos, tales como una Base de datos o 
un archivo.

Básicamente tenemos dos clases:
    1.  Cliente.py - Creación del objeto
    2.  ClienteDAO.py - Conversión del objeto en una consulta a la base de datos
        (Definidas debajo).
"""

from db_management.logger_base import *
from function_modules.Cliente import *
from db_management.Conexion import *
from db_management.cursor_del_pool import *

class ClienteDAO:
    _SELECCIONAR = 'SELECT * FROM cliente ORDER BY id_cliente'
    _INSERTAR = 'INSERT INTO cliente(nombre, apellido) VALUES(%s, %s)'
    _ACTUALIZAR = 'UPDATE cliente SET nombre = %s, apellido = %s WHERE id_persona = %s'
    _BORRAR = 'DELETE FROM persona WHERE id_persona = %s'

    @classmethod
    def seleccionar(cls):
        with CursorDelPool() as cursor:
            cursor.execute(cls._SELECCIONAR)
            registros = cursor.fetchall()
            clientes = []
            for registro in registros:
                cliente = Cliente(registro[0], registro[1], registro[2])
                clientes.append(cliente)
            return clientes
        
    @classmethod
    def insertar(cls, cliente):
        with CursorDelPool() as cursor:
            valores = (cliente.nombre, cliente.apellido)
            cursor.execute(cls._INSERTAR, valores)
            log.debug(f'Registro insertado en la base de datos: {cliente}')
            return cursor.rowcount
        
    @classmethod
    def actualizar(cls, cliente):
        with CursorDelPool() as cursor:
            valores = (cliente.nombre, cliente.apellido, cliente.id_cliente)
            cursor.execute(cls._ACTUALIZAR, valores)
            log.debug(f'Registro actualizado: {cliente}')
            return cursor.rowcount

    @classmethod
    def borrar(cls, cliente):
        with CursorDelPool() as cursor:
            valores = (cliente.id_cliente)
            cursor.execute(cls._BORRAR, valores)
            log.debug(f'Registro eliminado: {cliente}')
            return cursor.rowcount
        
# Módulo de pruebas para el módulo.
if __name__ == '__main__':
    # Insertar un registro
    cliente1 = Cliente(nombre = 'Alejandra', apellido = 'Téllez')
    clientes_insertados = ClienteDAO.insertar(cliente1)
    log.debug(f'Registro insertado en la base de datos: {clientes_insertados}')

    # Seleccionar objetos
    clientes = ClienteDAO.seleccionar()
    for cliente in clientes:
        log.debug(cliente)
