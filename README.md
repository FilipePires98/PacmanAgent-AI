# Pacman AI Agent
An Artificial Intelligent Agent that plays Pacman

![](https://img.shields.io/badge/Academical%20Project-Yes-success)
![](https://img.shields.io/badge/2018%20Competition-Winner%20Agent-yellow)
![](https://img.shields.io/badge/OS-Linux-blue)
![](https://img.shields.io/badge/Made%20with-Python-blue)
![](https://img.shields.io/badge/Maintained-No-red)

## Description

The purpose of this work is to develop an agent capable of playing in a clever way the Pacman game, an arcade game that has become popular in the last century.

Several agents competed for the highest score when exposed to other agents (the ghosts) implemented by professor [Diogo Gomes](https://github.com/dgomes) and other contributors.

Our Pacman was the **winner agent of 2018**. 

![demo](https://github.com/FilipePires98/PacmanAgent-AI/blob/master/docs/pacman_gameplay.gif)

## Repository Structure

/data - UI images (map and sprites)

/docs - License, presentation and gameplay demo

/prof - performance evaluation source code

/src - source code of our agent

/tests - test scripts

## Instructions to Install and Run

```console
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Open 3 terminals, in each terminal runonce:
```console
$ source venv/bin/activate
```
Run each application in it's terminal:

Terminal 1:
```console
$ python server.py
```
Terminal 2:
```console
$ python viewer.py
```
Terminal 3:
```console
$ python client.py
```

## Authors

The authors of the base code are mainly professores Diogo Gomes and Mario Antunes.
The authors of this specific implementation of the Pacman agent are Filipe Pires and João Alegria.

For further information, please contact us at fsnap@protonmail.com or joao.p@ua.pt.

# Credits
Sprites from https://github.com/rm-hull/big-bang/tree/master/examples/pacman/data
