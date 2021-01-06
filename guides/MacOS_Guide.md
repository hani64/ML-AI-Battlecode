# MacOS Local Testing Guide
    MacOS requires different settings than Ubuntu and Windows.
    Therefore, use mac_os_server along with mac_run.sh
    to run the server.

    Ensure that python3 is installed. This can be done however.

## Manual Testing:
1. Open 3 command prompts

2. Go to project root

3. Run Server (Project root)
    `python3  ./mac_os_server/server_runner.py 8888 --verbose`

4. Run Player 1 (From folder containing desire player1 client code)
    `python3  ./client_runner.py localhost 8888`

5. Run Player2 (From folder containing desire player2 client)
    `python3  ./client_runner.py localhost 8888`

## Automatic Testing:
1. Install homebrew
    Follow steps at: https://brew.sh/
2. Install tmux via homebrew
    ```
    brew install tmux
    ```
3. Deployment
    In the project root, run:
    ```
    ./mac_run.sh
    ```
