""" The local government class module """
from models import *
import json
from datetime import datetime
#from models import db
from functions import myfunctions as func
from appclasses.location import LOCATION


class LGA(object):
	"""This is the local government class"""
	lga_id = 0
	state_id = 0 	
	name = ""
	locations = None
	lga_obj = {}

	def __init__(self, data=None):
		"""Initialize the LGA class with data (dic) containing its name (str) and place IDs (int)"""
		super(LGA, self).__init__()
		if data is not None:
			self.name = data["name"].title() 			
			self.state_id = data["state_id"]
			self.locations = data["locations"] 			
			self.create_lga_obj()
			
	def create_lga_obj(self):
		""" creates the lga object that specificaly identifies the lga """
		self.lga_obj = {"name":self.name,"state_id":self.state_id}
		if func.object_exists("lga",self.lga_obj):
			self.lga_id = LocalGovt.query.filter_by(local_govt=self.name,state_id=self.state_id).first().id_no
			self.lga_obj["lga_id"] = self.lga_id
			if self.locations == None:
				self.locations = self.get_lga_locations()
		
	def add_lga(self):
		""" adds new lga record to database """				
		error = []
		obj = self.lga_obj									
		if not func.object_exists("lga",obj):			
			new = LocalGovt()
			new.local_govt = obj["name"].title()	 		
			new.state_id = obj["state_id"]
			db.session.add(new)
			db.session.commit()			
			self.lga_id = new.id_no
			status = func.alert(1)["status"]
			message = func.alert(1)["message"]
		else:
			self.lga_id = func.object_exists("lga",obj).id_no
			error.append({"err_code":5,"data":self.name})
			status = func.alert(2)["status"]
			message = func.alert(2)["message"]

		#add locations if data is available
		if self.locations is not None and len(self.locations) > 0:
			for location in self.locations:
				if func.validate_input(location,"add_location"):
					mr = {}
					mr["name"] = location["name"]
					mr["state_id"] = self.state_id
					mr["lga_id"] = self.lga_id
					mr["streets"] = location["streets"]
					log = LOCATION(mr)
					res = log.add_location()
					error.extend(res["error"])
				else:
					error.append({"err_code":4,"data":"{} locations data".format(self.name)})
							
		return {"status":status,"message":message,"error":error}

	def get_lga_locations(self):
		""" Returns all the locations with their streets that match lga ID """
		if self.lga_id > 0:
			loc = LOCATION()
			return loc.get_locations(self.lga_obj,"lga")
		else:
			return None
	
	def get_lgas(self,id,level=""):
		""" Returns all the lgas that match state ID in the data (dic) 
			level (str) defines the scope of the query
		"""		
		lga_data = []			 
		if level == "state":
			locs = LocalGovt.query.filter_by(state_id=id).all()
			
			for i in locs:
				getter = LOCATION()
				mr = {}
				mr["name"] = i.local_govt
				mr["locations"] = getter.get_locations(i.id_no,"lga")
				lga_data.append(mr)
					
			return lga_data
		else:
			locs = LocalGovt.query.all()
			for i in locs:
				getter = LOCATION()
				mr = {}
				mr["name"] = i.local_govt
				mr["locations"] = getter.get_locations(i.id_no,"lga")
				lga_data.append(mr)	
			return lga_data		
	
	def delete_lga_record(self, data):
		""" Deletes database record for the given lga including its locations and streets """
		
		if 	func.object_exists("state",{"name":data["state"]}):
			lga_id = func.object_exists("state",{"name":data["state"]}).id_no
							
			query = LocalGovt.query.filter_by(id_no=lga_id).first()			

			#delete all streets associated with the lga
			for i in query.linkstreet:
				Street.query.filter_by(strid=i.strid).delete()
				db.session.commit()
			#delete all locations associated with the lga
			for i in query.linklocation:
				Location.query.filter_by(loc_id=i.loc_id).delete()
				db.session.commit()			 

			#now delete the lga	
			LocalGovt.query.filter_by(id_no=lga_id).delete()
			db.session.commit()
			return func.alert(1)

		
		return func.alert(6)

	def updates_lga_record(self, new_record, data_by_name=None, data_by_id=None):
		""" Modifies database record for the given lga """
		if data_by_name is not None:
			data = data_by_name

			if 	func.object_exists("state",{"name":data["state"]}):
				self.state_id = func.object_exists("state",{"name":data["state"]}).id_no
				
				if func.object_exists("lga",{"name":data["lga"],"state_id":self.state_id}):
					query = func.object_exists("lga",{"name":data["lga"],"state_id":self.state_id})
					self.lga_id = query.id_no
					self.name = query.local_govt
					self.create_lga_obj()
					
					LocalGovt.query.filter_by(id_no=self.lga_id).update({"local_govt":new_record["name"].title()})
					db.session.commit()
					return func.alert(1)

		elif data_by_id is not None:			
			lga_id = func.object_exists("lga",data_by_id).id_no
			LocalGovt.query.filter_by(id_no=lga_id).update({"local_govt":new_record["name"].title()})
			db.session.commit()
			return func.alert(1)

		return func.alert(6)			