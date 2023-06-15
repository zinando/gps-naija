""" The street class module """
from models import Street, Location
import json
from datetime import datetime
from models import db
from functions import myfunctions as func


class STREET(object):
	"""This is the street class"""
	street_id = 0
	state_id = 0
	lga_id = 0
	location_id = 0
	name = ""
	street_obj = {}

	def __init__(self, data=None):
		"""Initialize the street class with data (dic) containing its name (str) and place IDs (int)"""
		super(STREET, self).__init__()
		if data is not None:
			self.name = data["name"].title()
			self.location_id = data["location_id"]
			self.lga_id = data["lga_id"]
			self.state_id = data["state_id"]
			self.create_street_obj() 			

	def create_street_obj(self):
		""" creates the street object that specificaly identifies the street """
		self.street_obj = {"name":self.name,"location_id":self.location_id,"lga_id":self.lga_id,"state_id":self.state_id}
		data = self.street_obj
		if func.object_exists("street",self.street_obj):
			self.street_id = Street.query.filter_by(streetname=data["name"],stateID=data["state_id"],lgaID=data["lga_id"],locID=data["location_id"]).first().strid
			self.street_obj["street_id"] = self.street_id

	def add_street(self):
		""" adds new street record to database """
		error = []
		street_obj = self.street_obj
		if self.street_id == 0:
			new = Street()
			new.streetname = street_obj["name"].title()
			new.locID = street_obj["location_id"]
			new.lgaID = street_obj["lga_id"] 
			new.stateID = street_obj["state_id"]
			db.session.add(new)
			db.session.commit()
			self.street_id = new.strid
			return {"status":1,"message":func.alert(1)["message"]}
		else:
			self.street_id = func.object_exists("street",street_obj).strid
			error.append({"err_code":5,"data":self.name})
			return {"status":2,"error":error}
	
	def get_street(self,id,level):
		""" Returns all the streets that match location IDs in the data (dic)
			level (str) defines the scope of the query  
		"""
		query = Street.query.all()
		count = 0
		for i in query:
			print(count+1,". ",i.streetname)
		print(len(query))
		if level == "location":
			return [x.streetname for x in Street.query.filter_by(locID=id).all()]
		elif level == "lga":
			return [x.streetname for x in Street.query.filter_by(lgaID=id).all()]
		elif level == "state":
			return 	[x.streetname for x in Street.query.filter_by(stateID=id).all()]		
			
	
	def delete_street_record(self, data):
		""" Deletes database record for the given street """
		if data_by_name is not None:
			data = data_by_name

			if 	func.object_exists("state",{"name":data["state"]}):
				self.state_id = func.object_exists("state",{"name":data["state"]}).id_no
				
				if func.object_exists("lga",{"name":data["lga"],"state_id":self.state_id}):
					self.lga_id = func.object_exists("lga",{"name":data["lga"],"state_id":self.state_id}).id_no
					
					if func.object_exists("location",{"name":data["location"],"state_id":self.state_id,"lga_id":self.lga_id}):
						self.location_id = func.object_exists("location",{"name":data["location"],"lga_id":self.lga_id,"state_id":self.state_id}).loc_id

						if func.object_exists("street",{"name":data["street"],"state_id":self.state_id,"lga_id":self.lga_id,"location_id":self.location_id}):
							self.street_id = func.object_exists("street",{"name":data["street"],"state_id":self.state_id,"lga_id":self.lga_id,"location_id":self.location_id}).strid

							Street.query.filter_by(strid=self.street_id).delete()
							db.session.commit()
							return func.alert(1)

		return func.alert(6)

	def update_street_record(self, new_record, data_by_name=None, data_by_id=None):
		""" Modifies database record for the given street """
		if data_by_name is not None:
			data = data_by_name

			if 	func.object_exists("state",{"name":data["state"]}):
				self.state_id = func.object_exists("state",{"name":data["state"]}).id_no
				
				if func.object_exists("lga",{"name":data["lga"],"state_id":self.state_id}):
					self.lga_id = func.object_exists("lga",{"name":data["lga"],"state_id":self.state_id}).id_no
					
					if func.object_exists("location",{"name":data["location"],"state_id":self.state_id,"lga_id":self.lga_id}):
						self.location_id = func.object_exists("location",{"name":data["location"],"lga_id":self.lga_id,"state_id":self.state_id}).loc_id

						if func.object_exists("street",{"name":data["street"],"state_id":self.state_id,"lga_id":self.lga_id,"location_id":self.location_id}):
							self.street_id = func.object_exists("street",{"name":data["street"],"state_id":self.state_id,"lga_id":self.lga_id,"location_id":self.location_id}).strid

							Street.query.filter_by(strid=self.street_id).update({"streetname":new_record["name"].title()})
							db.session.commit()
							return func.alert(1)

		elif data_by_id is not None:			
			street_id = func.object_exists("street",data_by_id).strid
			Street.query.filter_by(strid=street_id).update({"streetname":new_record["name"].title()})
			db.session.commit()
			return func.alert(1)

		return func.alert(6)					
