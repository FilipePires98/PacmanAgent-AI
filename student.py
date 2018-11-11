import random
import sys
import json
import asyncio
import websockets
import os
from mapa import Map
from Pacman import Pacman
from Tree import *

async def agent_loop(server_address = "localhost:8000", agent_name="student"):
    async with websockets.connect("ws://{}/player".format(server_address)) as websocket:

        # Receive information about static game properties 
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
        msg = await websocket.recv()

        game_properties = json.loads(msg) 
         
        mapa = Map(game_properties['map'])
        pacman=Pacman(mapa)
        #init agent properties 
        key = None
        cur_x, cur_y = None, None
        while True: 
            r = await websocket.recv()
            state = json.loads(r) #receive game state
            if len(state['energy'])==0:
                break
            if not state['lives']:
                print("GAME OVER")
                return

            x, y = state['pacman']

            #if pacman.isNode((x,y)) or key==None:
            eatGhost=False
            ghosts=[]
            eatableG=[]
            runG=[]
            for g in state['ghosts']:
            	eatGhost=eatGhost or g[1]
            	ghosts.append(g[0])
            	if g[1]==True:
            		eatableG.append(g[0])
            	else:
            		runG.append(g[0])

            p=SearchProblem(pacman, tuple(state['pacman']))
            t = SearchTree(p, state['energy'], state['boost'], ghosts)
            #print(len(state['energy']), len(state['boost']), len(ghosts))

            if eatGhost and len(ghosts)>0:
            	key=t.searchGhost(eatableG, runG)
            else:
            	key = t.search()
            '''
            if x == cur_x and y == cur_y:
                if key in "ad":
                    key = random.choice("ws")
                elif key in "ws":
                    key = random.choice("ad")
            cur_x, cur_y = x, y
            '''
            #send new key
            await websocket.send(json.dumps({"cmd": "key", "key": key}))


loop = asyncio.get_event_loop()
SERVER = os.environ.get('SERVER', 'localhost')
PORT = os.environ.get('PORT', '8000')
NAME = os.environ.get('NAME', '85048_85122')
loop.run_until_complete(agent_loop("{}:{}".format(SERVER,PORT), NAME))
