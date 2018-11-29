xterm -hold -e "source venv/bin/activate; python3.6 server.py --ghosts 4 --level 1" &
sleep 1
xterm -hold -e "source venv/bin/activate; python3.6 viewer.py --scale 2" &
max=1
for i in `seq 1 $max`
do
	xterm -hold -e "source venv/bin/activate; python3.6 student.py"
done

