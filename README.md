# Network-Manager
<table>
<tr>
<td>
  Flask server for Network management in GNS3.
</td>
</tr>
</table>

# Objective
<table>
<tr>
<td>
    Get information about devices in a Local Network (Name, Description, Location and Contact).
Information about packets sent in network using Pygal and Graphviz.
Alerts when packet loss with Tkinter
</td>
</tr>
</table>

# Table of contents

<!--ts-->
- [Network-Manager](#network-manager)
- [Objective](#objective)
- [Table of contents](#table-of-contents)
  - [Built with](#built-with)
  - [Functionalities](#functionalities)
  - [Demo](#demo)
  - [Site](#site)
  - [Mobile Support](#mobile-support)
  - [Installation](#installation)
  - [Tests](#tests)
  - [To-do](#to-do)
  - [Team](#team)
  - [License](#license)
<!--te-->

## Built with 
![Python 3.6.5](https://img.shields.io/badge/-Python3.6.5-05122A?style=flat&logo=python)
![Flask](https://img.shields.io/badge/-Flask-05122A?style=flat&logo=flask)
![Bootstrap](https://img.shields.io/badge/-Bootstrap-05122A?style=flat&logo=bootstrap&logoColor=563D7C)
![HTML](https://img.shields.io/badge/-HTML-05122A?style=flat&logo=HTML5)
![CSS](https://img.shields.io/badge/-CSS-05122A?style=flat&logo=CSS3&logoColor=1572B6)
![SQLite](https://img.shields.io/badge/-SQLite-05122A?style=flat&logo=SQLite&logoColor=white)

## Functionalities

- User Registration
- Login as general or admin user
- Roles management
- Create form in modal window by default
- Inline editing enabled by default
- Skins and  layout customization
- Dashboard, charts, chat and calendar examples
- Detects Network Topology and handle updates processes every x time (admin only)
- Graphs the Network Topology
  - Uses secure channel to communicate between them
  - Create, Modify & Delete Users
  - Raise dynamic routing protocols (RIP, OSPF and IGRP), admin can change the protocol and modify the parameters
  - MIB-II using SNMPv3
  - Can change
    - Host Name
    - OS Version
    - Admin
    - Location
    - Contact
    - Time up and last change
- Save in a DB the main network data and deploy PDF's and Graphs containing them
- Show:
  - Packages sent and received
  - Packages lost
  - Packages broken
- Save every event realized in a DB and see it in REST
- Send e-mails with changes
  - Percentage of lost packages / time
  - Broken packages / time
  - Device data Modification
  - Up or Down of the Interface

## Demo

Here is a working live demo: *Insert Demo Link Here*

## Site

Currently on Development.

## Mobile Support

The Network-Manager is compatible with devices of all sizes and all OS's.

Currently on Development.

## Installation

- Clone or download the git repository.

    ```sh
    git clone https://github.com/AdrianRomo/NetworkManager.git
    ```

- Create and activate a virtual environment:

    ```sh
    virtualenv venv
    $ source venv/bin/activate
    ```

- Install the requirements inside the app folder

    ```sh
    pip install -r requirements.txt
    ```

- Once the process finishes give execution permission to app.py file and run it

    ```sh
    ./app.py
    ```

- The first execution will create automatically a sample sqlite database.
- Open your favorite browser and type:

    ```
    https://localhost:5000/admin
    ```

    then just log in with the default user or register one.

## Tests

Currently on Development.

## To-do

On Development

## Team

[![Adrian Romo](https://avatars1.githubusercontent.com/u/17463208?v=4&s=144)](https://github.com/AdrianRomo)  | [![Jaime Lechuga](https://pkimgcdn.peekyou.com/8a3305196bab395057994e0b738029b8.jpeg)](https://github.com/JamesDLechu)
---|---|
[Adrian Romo](https://github.com/AdrianRomo) |[Jaime Lechuga](https://github.com/JamesDLechu)

## [License](https://github.com/AdrianRomo/LyricGenerator/blob/main/LICENSE)

MIT © [Adrian Romo](https://github.com/AdrianRomo)
