import random
import sys
import json
import asyncio
import websockets
import os
from mapa import Map
from Tree import *

async def agent_loop(server_address = "localhost:8000", agent_name="student"):
    async with websockets.connect("ws://{}/player".format(server_address)) as websocket:
        
        #recebe informacoes estaticas do jogo e mapa 
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
        msg = await websocket.recv()

        game_properties = json.loads(msg) 
         
        mapa = Map(game_properties['map'])
        ghosts_level = game_properties['ghosts_level']
        #print(game_properties)
        


        #propriedades iniciais do agente
        pacman=Pacman(mapa)
        key = None
        cur_x, cur_y = None, None
        map_center = None
        first_iteration = True

        while True: 
            r = await websocket.recv()
            state = json.loads(r) #recebe estado do jogo


            #verifica se o jogo acabou
            if len(state['energy'])==0 and len(state['boost'])==0:
                f=open("scores.csv", "a")
                f.write(str(state["score"]))
                f.write("\n")
                f.close()
                return 
            
            if not state['lives']:
                print("GAME OVER")
                f=open("scores.csv", "a")
                f.write(str(state["score"]))
                f.write("\n")
                f.close()
                return




            if not first_iteration:
                pastGhosts = runG[:]

            
            eatGhost=False
            ghosts=[]
            eatableG=[]
            runG=[]

            
            #adiciona o spawn dos ghosts
            if map_center==None and state['ghosts']!=[]:
                map_center = tuple(state['ghosts'][0][0])
            if map_center!=None:
                runG.append(map_center)


            #diferencia os ghosts possiveis de comer e os perigosos
            for g in state['ghosts']:
                eatGhost=eatGhost or g[1]
                ghosts.append(g[0])
                if g[1]==True:
                    eatableG.append(g)
                else:
                    runG.append(g[0])

            if first_iteration or (prevEatGhost==True and eatGhost==False):
                first_iteration = False
                pastGhosts = runG[:]


            #sorteia as energias para evitar os boosts se nao esta a ser perseguido
            prevEatGhost=eatGhost
            energies=[x for x in state['energy'] if all(abs(x[0]-y[0])+abs(x[1]-y[1])>3 for y in state['boost'])]
            if energies==[]:
                energies=state['boost']
            if any(abs(state['pacman'][0]-z[0][0])+abs(state['pacman'][1]-z[0][1])<3 for z in state['ghosts']):
                getBoost=True
            else:
                getBoost=False
            if energies==[]:
                energies=state['energy']


            #inicia o problema atual
            p = SearchProblem(pacman, tuple(state['pacman']))
            t = SearchTree(p, energies, state['boost'], runG, pastGhosts)
            

            #verifica se o jogo tem uma complexidade elevada
            if(ghosts_level==3 and len(ghosts)>2) or (ghosts_level==2 and len(ghosts)>2):
                eatableG=[x[0] for x in eatableG if not pacman.ghostInSafeZone(x) and (abs(state['pacman'][0]-x[0][0])+abs(state['pacman'][1]-x[0][1]))<x[2] and (abs(state['pacman'][0]-x[0][0])+abs(state['pacman'][1]-x[0][1]))<6]
            else:
                eatableG=[x[0] for x in eatableG if not pacman.ghostInSafeZone(x) and (abs(state['pacman'][0]-x[0][0])+abs(state['pacman'][1]-x[0][1]))<x[2]]

            #resolve o problema atual
            if eatGhost and len(ghosts)>0:
                eatableG = [eg for eg in eatableG if pacman.d8(eg,runG)] 
                if eatableG!=[]:
                    key = t.searchGhost(eatableG)
                else:
                    key = t.search(getBoost)
            else:
                key = t.search(getBoost)
            

            #send new key
            await websocket.send(json.dumps({"cmd": "key", "key": key}))

loop = asyncio.get_event_loop()
SERVER = os.environ.get('SERVER', 'localhost')
PORT = os.environ.get('PORT', '8000')
#SERVER = os.environ.get('SERVER', 'pacman-aulas.ws.atnog.av.it.pt')
#PORT = os.environ.get('PORT', '80')
NAME = os.environ.get('NAME', '85048_85122')
loop.run_until_complete(agent_loop("{}:{}".format(SERVER,PORT), NAME))
