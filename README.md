# BlackBoard

### About
A messaging application to demonstrate distributed computing. The project was developed during the lecture "Distributed Systems" at DHBW Ravensburg Campus Friedrichshafen. The group consists of Yannic, Ali, Elias, Lenny, Finn, Gabriel, and Christoph.

### Get Started
You can find the code for the BlackboardServer in `$ cd code\BlackboardServer\`. Start `app.py` with Python 3.12 (`$ python app.py`) for maximum compatibility. You will probably need to install some external dependencies, such as `$ pip install Flask`. You might also need to adjust your firewall settings to allow port 5000 usage.

A Flask server will start that serves the REST API on the IP address displayed in the command line. You can now access the API with our client in `$ cd code\BlackboardClient\` or write your own. To gracefully close the server, simply press `Ctrl+C`. While running the server, you can observe relevant events in the log file `log/blackboard.log`.

### Docs
For more information about the API, check out the `$ cd doc\` folder. There you can find information about our system architecture as well as supported API functions.

### Testing
Mainly for development purposes and function verification, we have written some tests (`$ py.test.exe`). These tests might also help you gather insights into how the application works from a client perspective and might be useful if you feel overwhelmed or disoriented, as some of us did (only in the beginning, of course).

#### Have Fun Scrolling & Deploying


# BlackBoard

### About
A messaging application to demonstrate distributed computing. The project was developed during the lecture "Distributed Systems" at DHBW Ravensburg Campus Friedrichshafen. The group consists of Yannic, Ali, Elias, Lenny, Finn, Gabriel, and Christoph.

### Get Started

1. **Clone the Repository:**
   `git clone https://github.com/yourusername/yourproject.git`
   `cd yourproject`

2. **Ensure Python 3.12 is Installed:**
   This project requires Python 3.12. Please ensure it is installed on your machine.

3. **Create and Activate the Virtual Environment:**

   - On Windows:
     `python -m venv venv_blackboard`
     `.\venv_blackboard\Scripts\activate`

   - On macOS and Linux:
     `python3 -m venv venv_blackboard`
     `source venv_blackboard/bin/activate`

4. **Install Dependencies:**
   `pip install -r requirements.txt`

5. **Start the Blackboard Server:**
   Navigate to the server directory and start the server:
   `python .\code\BlackboardServer\app.py`

   You might need to adjust your firewall settings to allow port 5000 usage.

   A Flask server will start that serves the REST API on the IP address displayed in the command line. You can now access the API with our client in `cd code\BlackboardClient` or write your own. To gracefully close the server, simply press `Ctrl+C`. While running the server, you can observe relevant events in the log file `log/blackboard.log`.

### Docs
For more information about the API, check out the `cd doc\` folder. There you can find information about our system architecture as well as supported API functions.

### Testing
Mainly for development purposes and function verification, we have written some tests (`$ py.test.exe`). These tests might also help you gather insights into how the application works from a client perspective and might be useful if you feel overwhelmed or disoriented, as some of us did (only in the beginning, of course).

#### Have Fun Scrolling & Deploying