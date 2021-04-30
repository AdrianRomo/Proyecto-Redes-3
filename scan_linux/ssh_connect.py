#!/usr/bin/env python3
from netmiko import ConnectHandler

"""
    @author:        Adrian González Pardo
    @date_update:   23/04/2021
    @github:        AdrianPardo99
"""

"""
    @args:
        <cisco> Es el diccionario que contiene los datos para la conexion
        <cmd> Es la lista de comandos que va a ejecutar netmiko
"""
def conectar(cisco,cmd):
    net_connect = ConnectHandler(**cisco)
    net_connect.enable()
    output=[]
    for i in range(len(cmd)):
        output.append(net_connect.send_command(cmd[i]))
    return output

"""
    A diferencia de la función de arriba esta puede interconectarse con
    routers con routers y no equipo a router, en forma de puente la conexión
    @args:
        <cisco> Es el diccionario que contiene los datos para la conexion
        <cmd> Es la lista de comandos que va a ejecutar netmiko
"""
def conectar_bridge(cisco,cmd):
    net_connect = ConnectHandler(**cisco)
    net_connect.enable()
    output=[]
    for i in range(len(cmd)):
        output.append(net_connect.send_command_timing(cmd[i]))
    return output
