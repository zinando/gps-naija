""" The location class module """
from models import Location
import json
from datetime import datetime
from models import db
from functions import myfunctions as func
from appclasses.streetclass import STREET


class LOCATION(object):
	"""This is the location class"""
	location_id = 0
	state_id = 0
	lga_id = 0
	name = ""
	streets = None
	location_obj = {}

	def __init__(self, data=None):
		"""Initialize the location class with data (dic) containing its name (str) and place IDs (int)"""
		super(LOCATION, self).__init__()
		if data is not None:
			self.name = data["name"].title()
			self.lga_id = data["lga_id"]
			self.state_id = data["state_id"]
			self.streets = data["streets"] 			
			self.create_location_obj()
			
	def create_location_obj(self):
		""" creates the location object that specificaly identifies the location """
		self.location_obj = {"name":self.name,"lga_id":self.lga_id,"state_id":self.state_id}
		if func.object_exists("location",self.location_obj):
			self.location_id = Location.query.filter_by(location=self.name,stateID=self.state_id,lgaID=self.lga_id).first().loc_id
			self.location_obj["location_id"] = self.location_id
			if self.streets == None:
				self.streets = self.get_location_streets()

	def add_location(self):
		""" adds new location record to database """
		error = []
		obj = self.location_obj
		if not func.object_exists("location",obj):
			new = Location()
			new.location = obj["name"].title()
			new.lgaID = obj["lga_id"] 
			new.stateID = obj["state_id"]
			db.session.add(new)
			db.session.commit()
			self.location_id = new.loc_id
			status = func.alert(1)["status"]
			message = func.alert(1)["message"]			
		else:
			self.location_id = func.object_exists("location",obj).loc_id
			error.append({"err_code":5,"data":self.name})
			status = func.alert(2)["status"]
			message = func.alert(2)["message"]

		#add streets if data is available
		if self.streets is not None and len(self.streets) > 0:
			if func.validate_input(self.streets,"add_street"):
				for street in self.streets:
					mr = {}
					mr["name"] = street
					mr["state_id"] = self.state_id
					mr["lga_id"] = self.lga_id
					mr["location_id"] = self.location_id
					log = STREET(mr)
					res = log.add_street()
					if res["status"] == 2:
						error.extend(res["error"])
			else:
				error.append({"err_code":4,"data":"{} streets data".format(self.name)})
								
		return {"status":status,"message":message,"error":error}

	def get_location_streets(self):
		""" Returns all the streets that match location ID """
		if self.location_id > 0:
			loc = STREET()
			return loc.get_street(self.location_obj,"location")
		else:
			return None
	
	def get_locations(self,id,level):
		""" Returns all the locations that match lga ID in the data (dic)
			level (str) defines the scope of the query  
		"""		
		location_data = []			 
		if level == "lga":
			locs = Location.query.filter_by(lgaID=id).all()
			for i in locs:
				getter = STREET()
				mr = {}
				mr["name"] = i.location
				mr["streets"] = getter.get_street(i.loc_id,"location")
				location_data.append(mr)	
			return location_data
		elif level == "state":
			locs = Location.query.filter_by(stateID=id).all()
			for i in locs:
				getter = STREET()
				mr = {}
				mr["name"] = i.location
				mr["streets"] = getter.get_street(i.loc_id,"location")
				location_data.append(mr)	
			return location_data			
	
	def delete_location_record(self, data):
		""" Deletes database record for the given location including its streets """
		
		if 	func.object_exists("state",{"name":data["state"]}):
			loc_id = func.object_exists("state",{"name":data["state"]}).id_no
			
			query = Location.query.filter_by(loc_id=loc_id).first()			

			#delete all streets associated with the lga
			for i in query.linkstreet:
				Street.query.filter_by(strid=i.strid).delete()
				db.session.commit()
			
			#now delete the location	
			Location.query.filter_by(loc_id=self.loc_id).delete()
			db.session.commit()
			return func.alert(1)

		
		return func.alert(6)

	def update_location_record(self, new_record, data_by_name=None, data_by_id=None):
		""" Modifies database record for the given location """
		if data_by_name is not None:
			data = data_by_name

			if 	func.object_exists("state",{"name":data["state"]}):
				self.state_id = func.object_exists("state",{"name":data["state"]}).id_no
				
				if func.object_exists("lga",{"name":data["lga"],"state_id":self.state_id}):
					self.lga_id = func.object_exists("lga",{"name":data["lga"],"state_id":self.state_id}).id_no
					
					if func.object_exists("location",{"name":data["location"],"state_id":self.state_id,"lga_id":self.lga_id}):
						query = func.object_exists("location",{"name":data["location"],"lga_id":self.lga_id,"state_id":self.state_id})
						self.location_id = query.loc_id
						self.name = query.location
						self.create_location_obj()						

						Location.query.filter_by(loc_id=self.location_id).update({"location":new_record["name"].title()})
						db.session.commit()
						return func.alert(1)

		elif data_by_id is not None:			
			location_id = func.object_exists("location",data_by_id).loc_id
			Location.query.filter_by(loc_id=location_id).update({"location":new_record["name"].title()})
			db.session.commit()
			return func.alert(1)

		return func.alert(6)				
