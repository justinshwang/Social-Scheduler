# Social Scheduler

�Meet� is a tkinter application in which users upload their personal schedules and find different �meet up� times based on their availability via various 
features for socializing and communicating using Python sockets. For example, a colored indicator will represent current availability (either available or not available) 
and users will be able to manipulate availability spontaneously should an emergency arise or if they simply need �personal time.� Users can also indicate
 how they would prefer to spend certain times of the day for different activities such as �socializing�, �work�, �sleeping,� and �eating�.

Application was reorganized and containerized using Docker. 

## Requirements
1) libraries within [requirements.txt](requirements.txt)


## Setup
1) Run Docker Compose in root folder to start up MySQL database and server. Before running check /app/settings.py for host and port.

    ```
    docker-compose up -d
    ```

    Server can also be started up in 'app' directory

    ```
    py app/server.py
    ```

2) Before launching clients, ensure that client IP matches that of server. Modify host and port if necessary in /app/settings.py, then launch client.py (both on two seperate command prompts/Terminals if on same device)  on a command prompt/Terminal. image_util and other necessary modules are included in folder "modules"

    ```
    py app/client.py
    ```

3) Next, on the same command prompt or window, enter Name (which must be Eric and subsequently for other user Justin), press enter. User will be prompted to update database with csv files contained in assets->schedules.

