""" The State class module """
from models import *
import json
from datetime import datetime
from models import db
from functions import myfunctions as func
from appclasses.lgaclass import LGA


class STATE(object):
	"""This is the STATE class"""
	state_id = 0 	
	name = ""
	capital = ""
	lgas = None
	state_obj = {}

	def __init__(self, data=None):
		"""Initialize the STATE class with data (dic) containing its name (str) and its capital """
		super(STATE, self).__init__()
		if data is not None:
			self.name = data["name"].title() 			
			self.capital = data["capital"].title()
			self.lgas = data["lgas"] 			
			self.create_state_obj()

	def create_state_obj(self):
		""" creates the STATE object that specificaly identifies the State """
		self.state_obj = {"name":self.name,"capital":self.capital}
		if func.object_exists("state",self.state_obj):
			self.state_id = State.query.filter_by(state=self.name).first().id_no
			self.state_obj["state_id"] = self.state_id
			if self.lgas == None:
				self.lgas = self.get_state_lgas()
			
	def add_state(self):
		""" adds new State record to database """				
		error = [] 
		obj = self.state_obj
		if not func.object_exists("state",obj):
			new = State()
			new.state = obj["name"].title()	 		
			new.capital = obj["capital"]
			db.session.add(new)
			db.session.commit()			
			self.state_id = new.id_no	 		
			status = func.alert(1)["status"]
			message = func.alert(1)["message"]
		else:
			self.state_id = func.object_exists("state",obj).id_no			
			error.append({"err_code":5,"data":self.name})
			status = func.alert(2)["status"]
			message = func.alert(2)["message"]

		#add lgas if data is available
		if self.lgas is not None and len(self.lgas) > 0:			
			for lga in self.lgas:
				if func.validate_input(lga,"add_lga"):					
					mr = {}
					mr["name"] = lga["name"]					
					mr["state_id"] = self.state_id				
					mr["locations"] = lga["locations"]					
					log = LGA(mr)
					res = log.add_lga()
					error.extend(res["error"])
				else:
					error.append({"err_code":4,"data":"{} lgas data".format(self.name)})

		return {"status":status,"message":message,"error":error}
				
	def get_state_lgas(self):
		""" Returns all the LGAs with their locations and streets that match State ID """
		if self.state_id > 0:
			loc = LGA()
			return loc.get_lgas(self.state_id,"state")
		else:
			return None

	def get_states(self,state_name=None):
		""" Returns all the States in Nigeria if no state name is provided """
		print("getting states")
		state_data = []
		if state_name is None:
			locs = State.query.all()
		else:
			locs = [State.query.filter_by(state=state_name.title()).first()]	

		for i in locs:
			getter = LGA()			
			mr = {}
			mr["name"] = i.state
			mr["capital"] = i.capital
			mr["lgas"] = getter.get_lgas(i.id_no,"state")
			state_data.append(mr)

		return state_data

	def get_state_info(self, state_name):
		""" Returns a particular State in Nigeria with state_name """
		self.name = state_name.title() if type(state_name) is str else state_name
		error = []
		state_data = None
		if func.object_exists("state",{"name":state_name}):
			state_data = self.get_states(self.name)
			status = 1
		else:
			error.append({"err_code":6,"data":self.name})
			status = 2

		return {"status":status, "error": error, "data": state_data}
	
	def delete_state_record(self, data):
		""" Deletes database record for the given State including its lgas, locations and streets """
		
		if 	func.object_exists("state",{"name":data["state"].lower()}):
			state_id = func.object_exists("state",{"name":data["state"].lower()}).id_no				
			query = State.query.filter_by(id_no=state_id).first()			

			#delete all streets associated with the State
			for i in query.linkstreet:
				Street.query.filter_by(strid=i.strid).delete()
				db.session.commit()
			#delete all locations associated with the State
			for i in query.linklocation:
				Location.query.filter_by(loc_id=i.loc_id).delete()
				db.session.commit()
			#delete all lgas associated with the State
			for i in query.linklga:
				LocalGovt.query.filter_by(id_no=i.id_no).delete()
				db.session.commit() 	 	 
			#now delete the State
			State.query.filter_by(id_no=state_id).delete()
			db.session.commit()
			return func.alert(1)		

		return func.alert(6)	

	def update_state_record(self, new_record, data_by_name=None, data_by_id=None):
		""" Modifies database record for the given State """
		if data_by_name is not None:
			data = data_by_name

			if 	func.object_exists("state",{"name":data["state"]}):
				query = func.object_exists("state",{"name":data["state"]})				
				self.state_id = query.id_no
				self.name = query.state
				self.capital = query.capital
				self.create_state_obj()

				State.query.filter_by(id_no=self.state_id).update({"state":new_record["name"].title(),"capital":new_record["capital"].title()})
				db.session.commit()
				return func.alert(1)

		elif data_by_id is not None:			
			state_id = func.object_exists("state",data_by_id).id_no
			State.query.filter_by(id_no=state_id).update({"state":new_record["name"].title(),"capital":new_record["capital"].title()})
			db.session.commit()
			return func.alert(1)

		return func.alert(6)	