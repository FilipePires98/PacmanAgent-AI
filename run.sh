xterm -hold -e "source venv/bin/activate; python server.py --ghosts 2 --level 0" &
sleep 1
xterm -hold -e "source venv/bin/activate; python viewer.py --scale 2" &
xterm -hold -e "source venv/bin/activate; python client.py" &
