xterm -hold -e "source venv/bin/activate; python3.6 server.py --ghosts 4 --level 3 --map data/map2.bmp" &
sleep 1
xterm -hold -e "source venv/bin/activate; python3.6 viewer.py --scale 2" &
max=5
for i in $(seq 1 $max)
do
	xterm -e "source venv/bin/activate; python3.6 student.py"
done
