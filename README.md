# BlackBoard

### About
A messaging application to demonstrate distributed computing. The project was developed during the lecture "Distributed Systems" at DHBW Ravensburg Campus Friedrichshafen. The group consists of Yannic, Ali, Elias, Lenny, Finn, Gabriel, and Christoph.

### Get Started

#### Server
You can find the code for the BlackboardServer in `$ cd code\BlackboardServer\`. To ensure all external dependencies are installed create a venv `$ python -m venv venvbb` in the root folder, activate it `$ .\venvbb\Scripts\activate` and install the needed dependencies with the command `$ pip install -r requirements.txt`. Start `app.py` with Python 3.12 (`$ python app.py`) in a venv for maximum compatibility. 
You might need to adjust your firewall settings on Start to allow port 5000 usage.
A Flask server will start that serves the REST API on the IP address displayed in the command line. To gracefully close the server, simply press `Ctrl+C`. While running the server, you can observe relevant events in the log file `code\BlackboardServer\blackboard.log` and on the Console.

#### Client
You can initialize our Client with `git submodule update --init --recursive --remote`.
You can now access the API with our client in `$ cd code\BlackboardClient\` or write your own. A precompiled .exe file for x64 Windows Systems is provided in this directoire as well. To start the client just type `$ .\crabking.exe -p 3000 -b 127.0.0.1` replacing 3000 with your port the server is trough and 127.0.0.1 with the ip address the server is running on. For more information you can always type `$ .\crabking.exe -h`. 

As soon as the client start you can display all available commands by just pressing enter or typing `help`. For example to get started and create a Blackboard simply type `create "My Blackboard" 100`. You can always exit the application by pressing `Ctrl+C` or typing `exit`.

To build the client for your specific system pleas follow the README.md file in the `code\BlackboardClient\` directory.

### Docs
For more information about the API, check out the `$ cd doc\` folder. There you can find information about our system architecture as well as supported API functions.

### Testing
Mainly for development purposes and function verification, we have written some tests (`$ py.test.exe`). These tests might also help you gather insights into how the application works from a client perspective and might be useful if you feel overwhelmed or disoriented, as some of us did (only in the beginning, of course).