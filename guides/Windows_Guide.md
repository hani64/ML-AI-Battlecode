# Windows Local Testing Guide
    The run.sh will not work as Windows is not supported by default, 
    although if running manually, you can use WSL(Windows Subsystem for Linux).
    On WSL you will be mounted into a virtual filesystem. Perform `cd /mnt` to enter your filesystem's root directory.
    Note: This guide only works for windows 10. There are ways to make deerhunt on other versions, but they are not officially supported.
## Setup
1. WSL(Windows Subsystem for Linux)
    Install WSL and use the ubuntu shell available from following 
    the steps available at: https://ubuntu.com/wsl

## Manual Testing
1. Open 3 Ubuntu shells ensure you use the Ubuntu installed from WSL)

2. Go to project root

3. Run Server (Project root)
    `python3  ./server/server_runner.py 8888 --verbose`

4. Run Player 1 (From folder containing desire player1 client code)
    `python3  ./client_runner.py localhost 8888`

5. Run Player2 (From folder containing desire player2 client)
    `python3  ./client_runner.py localhost 8888`

## Automatic testing
1. Update apt repositories and install dos2unix:
    ```
    sudo apt-get update
    sudo apt-get install dos2unix
    ```

2. Enable running the bash script on windows.
    ```bash
    dos2unix run.sh
    ```

3.   In the project root, run:
    ```bash
    ./run.sh
    ```