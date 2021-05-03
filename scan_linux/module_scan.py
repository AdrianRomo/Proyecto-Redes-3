#!/usr/bin/env python3
from detecta import *
from ssh_connect import *
import os
import re
import netifaces as ni
import json

"""
    @author:        Adrian González Pardo
    @date_update:   23/04/2021
    @github:        AdrianPardo99
"""

"""
    @args:
        <interface_name> Es el nombre de la interfaz que va a trabajar para escanear toda la red
        Para comunicación SSH v2
        <user> Es el usuario por defecto en los routers a la hora de realizar todos los escaners
        <password> Es el password por defecto de los routers
        <secret> Es la clave secret a la hora de conectarse al router
"""
def scan_by_interface(interface_name="tap0",user="admin",password="admin",secret="1234"):
    # Prototipo de conexión a router cisco
    cisco={
        "device_type":"cisco_xe",
        "ip":"",
        "username":user,
        "password":password,
        "secret":secret
    }
    # Obtienen el disccionario de los datos de la red
    dic_data=ni.ifaddresses(interface_name)
    if 2 not in dic_data:
        print("No hay una dirección IPv4 en la interfaz")
        return [-1,-1]
    dic_data=dic_data[2][0]
    print(f"\n---------About---------\n{interface_name}:{dic_data}")
    addr=list(map(int,dic_data["addr"].split(".")))
    net=list(map(int,dic_data["netmask"].split(".")))

    c=determinate_prefix(net)
    # Se obtiene el identificador de la subred
    idnet=get_id_net(addr,net)
    # Se obtiene la dirección de broadcast
    range_net=get_broadcast_ip(idnet,net)

    print(f"-------Scan Network:-------\n\tID: {arr_to_ip(idnet)}/{c}\n\tNetmask: {arr_to_ip(net)}\n\tBroadcast: {arr_to_ip(range_net)}")

    # Se prepara para hacer is_host_up
    ips=[idnet[0],idnet[1],idnet[2],idnet[3]+1]
    responde=scan_range(ips,range_net)


    # Se filtra por primera vez que solo los elementos que sean Cisco

    ciscos=[]
    for i in range(len(responde)):
        for k,v in responde[i].items():
            if "Cisco_Router_IOS" in v:
                ciscos.append(responde[i])
    #print(f"Solo routers cisco: {ciscos}")

    # Despues de todo lo que hace el modulo hay que conectarse por ssh o telnet
    #   a los dispositivos cisco
    cmd=["sh ip int | i Internet address","sh ip int br | include up","sh run | include hostname"]
    c=0
    red={}
    red_id={}
    net_router={}
    for i in ciscos:
        flag=False
        # Los datos del router (Interfaces)
        for k,v in i.items():
            print(f"-------Enviando comandos a router con ip: {k}-------")
            cisco["ip"]=k
            output=conectar(cisco,cmd)
            dir=re.split("\n|  Internet address is | ",output[0])
            inte=re.split("\n|YES NVRAM  up                    up|YES manual up                    up| ",output[1])
            host_cmd=output[2].split("hostname ")[1]
            direcciones=[]
            interf=[]
            for j in dir:
                if j!="":
                    direcciones.append(j)
            for j in inte:
                if j!="":
                    interf.append(j)
            if host_cmd in red.keys():
                flag=False
            else:
                flag=True
            if flag:
                iter={}
                iter_s={}
                for j in range(len(direcciones)):
                    iter[interf[(j*2)]]=direcciones[j]
                    sub=direcciones[j].split("/")
                    pr=sub[1]
                    sub=list(map(int,sub[0].split(".")))
                    sub=arr_to_ip(get_id_net(sub,create_masc_by_prefix(int(pr))))
                    iter_s[f"{interf[(j*2)]}-sub"]=sub
                red[host_cmd]=iter
                red_id[host_cmd]=iter_s
            dir.clear()
            inte.clear()
            direcciones.clear()
        # Scan de subredes del router
        if flag:
            for k,v in red.items():
                if 0 not in v.values():
                    for j,l in v.items():
                        red_e=l.split("/")
                        if red_e[0] in i.keys():
                            print(f"-------Exists the network scanning {red_e[0]}-------")
                        else:
                            net=create_masc_by_prefix(int(red_e[1]))
                            id=get_id_net(list(map(int,red_e[0].split("."))),net)
                            br=get_broadcast_ip(id,net)
                            if arr_to_ip(br)!=arr_to_ip(id):
                                ip=[id[0],id[1],id[2],id[3]+1]
                                print(f"-------Scan Network:-------\n\tID: {arr_to_ip(id)}\n\tNetmask: {arr_to_ip(net)}\n\tBroadcast: {arr_to_ip(br)}")
                                resp_r=scan_range(ip,br)
                                responde=responde+resp_r
                                # aca filtrar Equipos cisco
                                for a in range(len(resp_r)):
                                    for b,d in resp_r[a].items():
                                        if "Cisco_Router_IOS" in d:
                                            ciscos.append(resp_r[a])
                    net_router[k]=v
                red[k]={0:0}
    json_respond=json.dumps(responde,sort_keys=True,indent=4)
    json_routers=json.dumps(net_router,sort_keys=True,indent=4)
    json_id=json.dumps(red_id,sort_keys=True,indent=4)
    arr_conexiones=verifica_conectividad(red_id,responde)
    print(f"Host con respuesta:\n{json_respond}\n"
        f"Diccionario de routers:\n{json_routers}\n"
        f"Identificadores de red de cada interfaz:\n{json_id}\n"
        f"Interconexiones:\n{arr_conexiones}")

    conexiones_r=[]
    for k,v in net_router.items():
        host_n={"hostname":k,"interfaces":[]}
        inter=[]
        for w,x in v.items():
            b=red_id[k][f"{w}-sub"]
            net=arr_to_ip(create_masc_by_prefix(int(x.split("/")[1])))
            prefix=int(x.split("/")[1])
            b=f"{b}/{prefix}"
            a={"name":w,
                "ip":x.split("/")[0],
                "netmask":net,
                "idnet":b}
            inter.append(a)
        host_n["interfaces"]=inter
        conexiones_r.append(host_n)
    json_conexiones=json.dumps(conexiones_r,sort_keys=True,indent=4)
    print(f"Información general:\n{json_conexiones}")
    # Posición 0 devuelve el json de todas las interfaces acomadado
    # Posición 1 devuelve el arreglo de interconexiones que hay entre routers
    # Posicion 2 devuelve todos los host que responsidieron al ping
    return [conexiones_r, arr_conexiones, net_router, responde]
    #return [json_conexiones,arr_conexiones,json_respond]
