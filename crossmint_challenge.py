from enum import StrEnum
from collections import namedtuple
import requests
import json
import time

ROWS = 30
COLUMNS = 30

CANDIDATE_ID = "24838118-0393-4b6a-a6ab-c6a309a10386"
API_URL_STRING = "https://challenge.crossmint.io/api/"
POLYANET_API_URL_STRING = "https://challenge.crossmint.io/api/polyanets/"
SOLOON_API_URL_STRING = "https://challenge.crossmint.io/api/soloons/"
COMETH_API_URL_STRING = "https://challenge.crossmint.io/api/comeths/"
GOAL_API_URL_STRING = f"https://challenge.crossmint.io/api/map/{CANDIDATE_ID}/goal"


class Color(StrEnum):
    WHITE = 'WHITE'
    PURPLE = 'PURPLE'
    BLUE = 'BLUE'
    RED = 'RED'

class Direction(StrEnum):
    LEFT='LEFT'
    RIGHT='RIGHT'
    UP='UP'
    DOWN='DOWN'

Polyanet = namedtuple('Polyanet', ['row', 'column'])
Soloon = namedtuple('Soloon', ['row', 'column', 'color'])
Cometh = namedtuple('Cometh', ['row', 'column', 'direction'])

###################
# POLYANET 
###################
def insert_polyanet(row: int, column: int):
    data={'candidateId' : CANDIDATE_ID, 'row' : row, 'column' : column}
    headers = {'content-type':'application/json'}

    resp = requests.post(url=POLYANET_API_URL_STRING, headers=headers, data=json.dumps(data))

    print(resp.status_code)
    print(resp.json())

def insert_polyanet(p: Polyanet):
    data={'candidateId' : CANDIDATE_ID, 'row' : p.row, 'column' : p.column}
    headers = {'content-type':'application/json'}

    resp = requests.post(url=POLYANET_API_URL_STRING, headers=headers, data=json.dumps(data))

    print(resp.status_code)
    print(resp.json())

def delete_polyanet(row: int, column: int):
    data={'candidateId' : CANDIDATE_ID, 'row' : row, 'column' : column}
    headers = {'content-type':'application/json'}

    resp = requests.delete(url=POLYANET_API_URL_STRING, headers=headers, data=json.dumps(data))

    print(resp.status_code)
    print(resp.json())


#################
# SOLOON
#################
def insert_soloon(s: Soloon):
    data={'candidateId' : CANDIDATE_ID, 'row' : s.row, 'column' : s.column, 'color' : str(s.color).lower()}
    headers = {'content-type':'application/json'}

    resp = requests.post(url=SOLOON_API_URL_STRING, headers=headers, data=json.dumps(data))

    print(resp.status_code)
    print(resp.json())

def delete_soloon(row: int, column: int):
    data={'candidateId' : CANDIDATE_ID, 'row' : row, 'column' : column}
    headers = {'content-type':'application/json'}

    resp = requests.delete(url=SOLOON_API_URL_STRING, headers=headers, data=json.dumps(data))

    print(resp.status_code)
    print(resp.json())

#################
# COMETH
#################
def insert_cometh(c: Cometh):
    data={'candidateId' : CANDIDATE_ID, 'row' : c.row, 'column' : c.column, 'direction': str(c.direction).lower()}
    headers = {'content-type':'application/json'}

    resp = requests.post(url=COMETH_API_URL_STRING, headers=headers, data=json.dumps(data))

    print(resp.status_code)
    print(resp.json())

def delete_cometh(row, column):
    data={'candidateId' : CANDIDATE_ID, 'row' : row, 'column' : column}
    headers = {'content-type':'application/json'}

    resp = requests.delete(url=COMETH_API_URL_STRING, headers=headers, data=json.dumps(data))

    print(resp.status_code)
    print(resp.json())

##################
# MISC
##################
def polyanet_cross():
    for i in range(2,9):
        # i,i
        insert_polyanet(i, i)
        time.sleep(1)
        # i, 11 - i
        insert_polyanet(i, COLUMNS-i-1)
        time.sleep(1)

def retreive_goal():
    headers = {'content-type':'application/json'}

    resp = requests.get(url=GOAL_API_URL_STRING, headers=headers)

    print(resp.status_code)
    json_response = resp.json()
    print(json_response)
    return json_response['goal']

# ingests the raw response from the goal
# NOTE: right now ROWS and COLUMNS are hardcoded constants. this is pretty easy to change if it needs to be changed, but not ideal.
def parse_goal(space_map):
    result = []
    for i in range(ROWS):
        for j in range(COLUMNS):
            cosmic_body = space_map[i][j]
            print(f"{cosmic_body} row:{i} col:{j}")
            
            if cosmic_body == 'POLYANET':
                # polyanets only have coordinates
                p = Polyanet(i, j)
                result.append(p)
                print(f"inserting polyanet {p}")

            elif 'SOLOON' in cosmic_body:
                sol = cosmic_body.split('_')
                # soloons have coordinates and a color
                s = Soloon(i, j, Color(sol[0]))
                result.append(s)
                print(f"inserting soloon {s}")

            elif 'COMETH' in cosmic_body:
                # comeths have coordinates and a directionality
                com = cosmic_body.split('_')
                c = Cometh(i, j, Direction(com[0]))
                result.append(c)
                print(f"inserting cometh {c}")
    
    print(f"number of cosmic bodies: {len(result)}")
    return result

# this function actually builds the megaverse
def build_megaverse(cosmic_body_list):
    
    for body in cosmic_body_list:
        time.sleep(1)
        
        if isinstance(body, Polyanet):
            insert_polyanet(body)

        elif isinstance(body, Soloon):
            insert_soloon(body)

        elif isinstance(body, Cometh):
            insert_cometh(body)
        


# Pull the goal
space_map = retreive_goal()
# parse the goal
cosmic_body_list = parse_goal(space_map)
print(cosmic_body_list)

build_megaverse(cosmic_body_list)