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
        #print(game_properties)
        pacman=Pacman(mapa)
        #init agent properties 
        key = None
        cur_x, cur_y = None, None
        map_center = None
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

            if map_center==None and state['ghosts']!=[]:
                map_center = tuple(state['ghosts'][0][0])
            if map_center!=None:
                runG.append(map_center)

            for g in state['ghosts']:
            	eatGhost=eatGhost or g[1]
            	ghosts.append(g[0])
            	if g[1]==True:
            		eatableG.append(g[0])
            	else:
            		runG.append(g[0])

            p = SearchProblem(pacman, tuple(state['pacman']))
            t = SearchTree(p, state['energy'], state['boost'], ghosts)
            #print(len(state['energy']), len(state['boost']), len(ghosts))
            '''
            if eatGhost and len(ghosts)>0:
                eatableG = [eg for eg in eatableG if pacman.d8(eg,runG)] 
                if eatableG!=[]:
                    key=t.searchGhost(eatableG, runG)
                else:
                    key = t.search()
            else:
                key = t.search()
            '''
            key=t.searchGhost(state['boost'], runG)
            #send new key
            await websocket.send(json.dumps({"cmd": "key", "key": key}))

            final_score = state['score']
    f=open("scores.txt", "a")
    f.write(str(final_score)+"\n")
    f.close()


loop = asyncio.get_event_loop()
SERVER = os.environ.get('SERVER', 'localhost')
PORT = os.environ.get('PORT', '8000')
NAME = os.environ.get('NAME', '85048_85122')
loop.run_until_complete(agent_loop("{}:{}".format(SERVER,PORT), NAME))
