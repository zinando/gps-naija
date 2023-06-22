# GPS-naija API Project
![GPS-naija API Banner image](static/assets/images/gps-naija.JPG)

## Project Description
In this project, i created a RESTful API with Flask. It is a backend app with a database integration and routes for communicating with clients. Its main purpose is to provide clients with names of places in Nigeria organized into States, LGAs, Locations (major landmarks) and Streets. These data have already been prestored and constantly updated in the database.

* Deployed Project Link: [gps-naija](https://gps-naija.onrender.com)
* Blog Post: [gps-naija](https://www.linkedin.com/posts/samuel-nnadozie-38349476_gps-naija-is-a-restful-api-that-serves-names-activity-7076487358199607296-qqKS?utm_source=share&utm_medium=member_desktop)

* Author: [Samuel Nnadozie](https://www.linkedin.com/in/samuel-nnadozie-38349476)

## Description of the routes:
There are two main routes that handle client requests from frontend. These are:

# /states: 
This route does not require any argument, and it returns a dictionary in which is contained data of all the States in Nigeria. 

# /states/state_name:
This route takes <b>state_name</b> as argument and returns a dictionary in which is contained data of the State with the name <b>state_name</b>.

## Description of the response:
Response from the API is a json-formatted dictionary object with three keys: <b>status</b>, <b>data</b>, and <b>error</b>. It must be parsed with an appropriate method before data could be accessed from it.
The value of the <b>status</b> key is a string and coud either be <i>success</i> or <i>error</i> depending on the result of the request.

The <b>error</b> key has a dictionary value. Its main purpose is to provide clear description of any error that might have occured during the processing of the client request. It has two keys:
- errors (list): holds each instance of error that occured during the processing of the request. An instance of an error with <b>error_code</b> and <b>data</b> as keys. Error_code is an integer which represents the type of error that occured, while data is a list containing data being prcessed when the error occured.
- legend (dictionary): holds the decription of different types of error that coud occure during request processing. The error_codes are the keys while the descriptions of the errors are their corresponding values.
When the status of the request is <i>success</i>, the value of the <b>error</b> key is just {}.

The <b>data</b> key holds the data (a list) being requested for. If the request is to get a single State data, the data is a list containing a dictionary of data about the State requested for. If the request is to get ALL the States, then data is a list of dictionaries of data about the all the States in Nigeria and FCT.

Each dictionary contains a State's data. It has the following keys: 
- <b>name</b> (string): name of the State
- <b>capital</b> (string): capital of the State
- <b>lgas</b> (list of dictionaries): contains data of all Local Government Areas in the State. Each instance of the lgas is a dictionary with <b>name</b> and <b>locations</b> as keys. The name represents the name of the local governmentm, while locations is a dictionary list of all locations (major landmarks) in the local government area. Each instance of the the locations is a dictionary with <b>name</b> and <b>streets</b> as keys. As usual, name is the location name while streets is a list of the names of all the streets in that location.

## Tech Stack :poodle:

<p align="center">
  <img src="https://github.com/zinando/gps-naija/blob/main/static/assets/images/arch.PNG"
       alt="GPS-naija Tech Stack"
       width="600"
  />
</p>

## Dependencies
| Tool/Library                                                            | Version |
| ----------------------------------------------------------------------- | ------- |
| [PYTHON](https://www.python.org/)                                       | 3.10.2  |
| [Flask](https://flask.palletsprojects.com/)                             | 2.3.2   |
| [SQLAlchemy](https://sqlalchemy.org/)                                   | 2.0.15  |
| [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)       | 3.0.3   |
| [gunicorn](https://gunicorn.org)                                        | 20.10.0 |

View the complete list of the dependencies in the [requirements.txt](requirements.txt) file.

## How to use the API:
You can use the API in any application freely by using the appropriate endpoints in your request.

# Endpoints for getting all the States data in Nigeria
- url : https://gps-naija.onrender.com/states
- H : {'Content-Type':'applicationjson'}
- X : GET


# Endpoints for getting a particular State data in Nigeria
- url : https://gps-naija.onrender.com/states/<arg>
- H : {'Content-Type':'applicationjson'}
- X : GET
- arg : name of the State

Example:

You can use any application of your choice that allows you to make http requests. The examples below were 
carried out using python programming language.

To get all States data from the API

```
	import requests

	url = 'https://gps-naija.onrend.com/states'
	headers = {"Content-Type":"application/json"}
	response = requests.get(url, headers = headers)
```

To get one State data from the API e.g Lagos State

```
	import requests

	url = 'https://gps-naija.onrend.com/states/lagos'
	headers = {"Content-Type":"application/json"}
	response = requests.get(url, headers = headers)
```

Accessing the information contained in the response:

```
	#parse the response
	data = response.json()

	#to know the status of the request
	print(data['status'])

	#to view the error if the status is 'error'
	print(data['error'])

	#to access the State data if the request is successful
	state_data = data['data']

	#loop through state_data to access information for each State
	for state in state_data:
		state_name = state['name']
		capital = state['capital']
		print("{} : {}".format(state_name, capital))

		#get all the LGA datain the State
		lgas = state['lgas']

		#loop through lgas to access information for each LGA
		for lga in lgas:
			lga_name = lga['name']
			print(lga_name)

			#get all locations within the LGA
			locations = lga['locations'] 

			#loop through locations to access information for each location
			for loc in locations:
				location_name = loc['name']
				print(location_name)

				#get all the Streets within the location
				streets = loc['streets']

				#loop through streets to access each street name
				for street in streets:
					print(street) 
```

## Authors

Ndubumma Samuel | Email: [samuel](mailto:belovedsamex@yahoo.com) | Github: [zinando](https://github.com/zinando)

## Contributors
Contributors are welcome to populate gps-naija database with more data of names of Locations and Steet names in each location. State names and LGAs have been completed already.
If you know names of streets in your location that are not already listed in our database, please send us the list following the instructions below:

```
	[{
		'name':'name of state',
	   'capital':'capital of the state',
	   'lgas':[
	   			'name': 'name of LGA',
	   			'locations':[
	   							'name':'name of location',
	   							'streets':['street name 1', 'street name 2', 'street name 3'....]
	   			]
	   ]
	}]     
```

Copy the data and send it as an email to zinando2000@gmail.com
I will process the data and then update gps-naija database with it
Also include in your email a link to any of your desired social media accounts so could referrence it when i'm listing your name in the contributors list both here and on the project's anding page.  	