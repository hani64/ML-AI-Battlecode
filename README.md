# Game
## How to submit
   You only need to submit your copy of =grid_player.py= and any new
   files that you created. You do *not* need to submit any of the helper
   classes that are provided to you. Your files should be at the root of
   the zip. You can achieve this by running the following command wherever
   your code is:

   #+BEGIN_SRC bash
     zip submission.zip grid_player.py 
   #+END_SRC

   To verify that you've zipped correctly you can either =vim submission.zip=
   and ensure that there is no folder only files or simply unzip your submission
   and confirm that no folders are created.

** Requirements
1. python3
2. bash shell.

## General Testing Guide
Below is a general guide of how different kinds of testing work. Please **Read the guide for your OS**. The supported OS' are **Windows, Ubuntu, and MacOs**. You will find their respective guides **in the `./guides` folder**.

The flag server which is run via `python3 ./<server_folder>/server_runner.py localhost <port> [--verbose]` where the verbose flag enables the printing of the map.
The verbose flag also ensures that once clients have computed you must press enter in the terminal to see the next tick be computed.

Note, there is a timeout on the server. If you do not connect your clients within the 
7 seconds from eachother, you will have to restart the server.

### Local Testing - Automated
   Enclosed is a `run.sh` file. This script automatically will run the server
   as well as both of the clients inside `tmux` (you need `tmux` installed for
   the script to work). You can run the script by typing `./run.sh 8888`. You 
   may need to change the port number if you're running the script frequently.

   The script will open `tmux` launch the server, then make a new tab and launch
   your client twice. You can navigate between the tabs by pressing =C-b n= (control b then n).

### Local Testing - Manual
   Alternatively you can launch the server and two clients manually in 3 seprate terminals.
   To do so, you will use `./server/server_runner.py` (Mac has a seperate server) and `./client/client_runner.py`
   from within `.`(root) and `./client` respectively.
   To tips on how to navigate directories with your terminal, you may find https://help.ubuntu.com/community/UsingTheTerminal 
   to be of use.

#### General Manual Steps
1. Open 3 terminals (Windows users ensure use Ubuntu installed WSL)

2. Go to project root

3. Run Server on terminal 1(within root)
   `python3  ./<server>/server_runner.py 8888` where server is "server" and "mac_os_server".

4. Run Player 1 terminal 2(From folder containing desire player1 client)
   `python3  ./client_runner.py localhost 8888` In a 

5. Run Player2 terminal 3(From folder containing desire player2 client)
   `python3  ./client_runner.py localhost 8888`
