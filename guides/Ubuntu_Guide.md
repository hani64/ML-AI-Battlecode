# Ubuntu Local Testing Guide

## Setup
1. Install python3
    `sudo apt-get update`
    `sudo apt-get install python3`

2. Install tmux
    `sudo apt-get install tmux`

3. Testing
    Choose a desired testing method below, and follow the listed steps.

## Manual Testing
1. Open 3 terminals.

2. Go to project root.

3. Run Server (Project root)
    `python3  ./server/server_runner.py 8888 --verbose`

5. Run Player 1 (From folder containing desire player1 client code)
    `python3  ./client_runner.py localhost 8888`

6. Run Player2 (From folder containing desire player2 client)
    `python3  ./client_runner.py localhost 8888`

## Automatic Testing
1.  In the project root, run:
    ```bash
    ./mac_run.sh
    ```
