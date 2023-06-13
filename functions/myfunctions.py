""" Contains functions that help to implement CRUD
"""
from flask import Flask, request
from datetime import datetime
from models import *


def format_date(date_str):
	""" Converts datetime str to datetime object 
		 Strictly processes only two formats: yyyy/mm/dd or yyyy-mm-dd 			
	"""
	date_obj = None
	try:
		date_obj = datetime.strptime(str(date_str), "%Y-%m-%d %H:%M:%S")
	except:
		date_obj=datetime.strptime(str(date_str), "%Y/%m/%d %H:%M:%S")

	return date_obj	

def object_exists(type,data):
	""" Checks if name of a place exists in the database
		 data: dic, name and location IDs of the place 
		 type: str, tells if name is state,lga,location or street
		 Returns True if it exists, otherwise False 
	"""
	if type == "street":
		return Street.query.filter_by(streetname=data["name"].title(),locID=data["location_id"],lgaID=data["lga_id"],stateID=data["state_id"]).first()		
	if type == "location":
		return Location.query.filter_by(location=data["name"].title(),lgaID=data["lga_id"],stateID=data["state_id"]).first()
	if type == "lga":
		return LocalGovt.query.filter_by(local_govt=data["name"].title(),state_id=data["state_id"]).first()
	if type == "state":
		return State.query.filter_by(state=data["name"].title()).first()
		
def alert(id):
	""" Returns an alert message confirming the status of and operation depending on the ID
		 1: all successful operations
		 2: database record insertion operation
		 3: database record modification operation
		 4: for wrong data format/type 
	"""
	if id == 1:
		return {"status":1,"message":"Operation was successful.","data":None}
	elif id == 2:
		return {"status":2,"message":"No records were added to database","data":None}
	elif id == 3:
		return {"status":3,"message":"No record was modified in the database.","data":None}
	elif id == 4:
		return {"status":4,"message":"Wrong data format","data":None}
	elif id == 5:
		return {"status":5,"message":"Record already exists","data":None}
	elif id == 6:
		return {"status":6,"message":"Record does not exist","data":None}			

def validate_input(data,input_for):
	""" Validates that an input is of appropriate type and contains the correct elements """
	if input_for == "add_state":
		#a dic which must contain the ffg keys: name, capital and lgas
		if type(data) is dict:			
			if {"name", "capital","lgas"}.issubset(data.keys()):
				return True
		return False		
	elif input_for == "add_lga":
		#a dic which must contain the ffg keys: name, locations
		if type(data) is dict: 
			if {"name", "locations"}.issubset(data.keys()):
				return True
		return False
	elif input_for == "add_location":
		#a dic which must contain the ffg keys: name, streets
		if type(data) is dict: 
			if {"name", "streets"}.issubset(data.keys()):
				return True
		return False
	elif input_for == "add_street":
		#a list 
		if type(data) is list:
			if type(data[0]) is str:
				return True
		return False

	elif input_for == "del_record":
		if type(data) is dict and {"what","id"}.issubset(data.keys()):					 	
			if  data["what"] == "state":
				#a dic
				if type(data["id"]) is dict:
					if {"state"}.issubset(data["id"].keys()):
						return True						
			elif data["what"] == "state_lga":
				#a dic
				if type(data["id"]) is dict:
					if {"state","lga"}.issubset(data["id"].keys()):
						return True						
			elif data["what"] == "state_lga_location":
				#a dic
				if type(data["id"]) is dict:
					if {"state","lga","location"}.issubset(data["id"].keys()):
						return True				
			elif data["what"] == "state_lga_location_street":
				#a dic
				if type(data["id"]) is dict:
					if {"state","lga","location","street"}.issubset(data["id"].keys()):
						return True 				
		return False

	elif input_for == "edit_record":
		if type(data) is dict and {"what","id","new"}.issubset(data.keys()):					 	
			if  data["what"] == "state":
				#a dic
				if type(data["id"]) is dict and type(data["new"]) is dict:
					if {"state"}.issubset(data["id"].keys()) and {"name","capital"}.issubset(data["new"].keys()):
						return True						
			elif data["what"] == "state_lga":
				#a dic
				if type(data["id"]) is dict and type(data["new"]) is dict:
					if {"state","lga"}.issubset(data["id"].keys()) and {"name"}.issubset(data["new"].keys()):
						return True						
			elif data["what"] == "state_lga_location":
				#a dic
				if type(data["id"]) is dict and type(data["new"]) is dict:
					if {"state","lga","location"}.issubset(data["id"].keys()) and {"name"}.issubset(data["new"].keys()):
						return True				
			elif data["what"] == "state_lga_location_street":
				#a dic
				if type(data["id"]) is dict and type(data["new"]) is dict:
					if {"state","lga","location","street"}.issubset(data["id"].keys()) and {"name"}.issubset(data["new"].keys()):
						return True 				
		return False	
							
def error_legend():
	legend = {
					"1": "Operation was successful",
					"2": "No records were added to database",
					"3": "No record was modified in the database.",
					"4": "Wrong data format",
					"5": "Record already exists",
					"6": "Record does not exist"
	}
	return legend				 					 												 


