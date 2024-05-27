# BlackBoard
### About
A massage application to demonstrate distributed computing.
The Project was developed during the Lecture "Distributed Systems" at DHBW Ravensburg Campus Friedrichshafen.
The Group consists of Yannic, Ali, Elias, Lenny, Finn, Gabriel and Christoph.

### Get Started
You can find the Code for the BlackboardServer in `$ cd code\BlackboardServer\`. Start app.py with Python3.12 (`$ python app.py`) for maximum Compatibility.
You probably have to pull some external Depedencies like `$ pip install Flask`.
You might have to calm your Firewall down regarding port usage.
A Flask Server will start that serves the RestAPI on the IP-Address displayed in the commandline.
Now you can access the API with our Client in `$ cd code\BlackboardClient\` or write your own.
### Docs
For more Information about the API check out the `$ cd doc\` folder. There you can find Information about our System Architecture as well as supported API functions.
### Testing
Mainly for development purposes and function verification we did write some Tests(`$ py.test.exe`). They might also help gather insights into how the Application works from a Client Perspective and might be therefore useful if you feel overwhelmed or without orientation like some of us might have (only in the beginning of course).
#### Have Fun Scrolling & Deploying