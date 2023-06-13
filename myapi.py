""" This is the main programme file
"""
from flask import Flask, request
from models import *
from functions import myfunctions as func
from appclasses.stateclass import STATE
import json
from appclasses.lgaclass import LGA
from appclasses.location import LOCATION
from appclasses.streetclass import STREET


@app.route('/states', methods=['GET', 'POST', 'DELETE', 'PUT'])
def states_route():
    """ Main route that exposes data of all States in Nigeria.
        With a GET request, it returns a dataset of all states in Nigeria
        With a POST request, new State record(s) is/are created 
    """    
    if request.method == 'GET':
        #get State record from the database
        #db.create_all()        
        worker = STATE()
        state_data = worker.get_states()              
        return json.dumps({"status":"success","data":state_data,"error":{}})

    elif request.method == "POST":
        #add State record to the database 
        #State.query.delete()
        #LocalGovt.query.delete()
        #db.session.commit()
        #return json.dumps({"status":"success","data":2,"error":{}})        
        json_data = request.get_json(force=True)
        error = []

        if type(json_data) is list:
            for data in json_data:
                if func.validate_input(data,"add_state"):
                    worker = STATE(data)
                    create = worker.add_state()
                    error.extend(create["error"])                    
                else:
                    error.append({"err_code":4,"data":data})      
        else:
            error.append({"err_code":4,"data":json_data})

        if len(error) > 0:
            mr = {}
            mr["legend"] = func.error_legend()
            mr["errors"] = error
            status =  "error"            
        else:
            status = "success"
            mr = {}                                
        return json.dumps({"status":status,"error":mr})

    elif request.method == "DELETE":
        #delete State record from the database
        error = []
        json_data = request.get_json(force=True)
        #record_to_delete = json_data["what"] #e.g state,state_lga,state_lga_location,state_lga_location_street
        if func.validate_input(json_data,"del_record"):
            if json_data["what"] == "street":
                worker = STREET()
                response = worker.delete_street_record(data=json_data["id"])
                if response["status"] > 1:
                    error.append({"err_code":6,"data":json_data})
            elif json_data["what"] == "location":
                worker = LOCATION()
                response = worker.delete_location_record(data=json_data["id"])
                if response["status"] > 1:
                    error.append({"err_code":6,"data":json_data})
            elif json_data["what"] == "lga":
                worker = LGA()
                response = worker.delete_lga_record(data=json_data["id"])
                if response["status"] > 1:
                    error.append({"err_code":6,"data":json_data})
            elif json_data["what"] == "state":
                worker = STATE()
                response = worker.delete_state_record(data=json_data["id"])
                if response["status"] > 1:
                    error.append({"err_code":6,"data":json_data})                                    
        else:
            error.append({"err_code":4,"data":json_data})      

        if len(error) > 0:
            mr = {}
            mr["legend"] = func.error_legend()
            mr["errors"] = error
            status =  "error"            
        else:
            status = "success"
            mr = {}                                
        return json.dumps({"status":status,"error":mr}) 

    elif request.method == "PUT":
        #update State record in the database
        error = []
        json_data = request.get_json(force=True)
        #record to update : json_data["what"] e.g state,state_lga,state_lga_location,state_lga_location_street
        #new record : json_data["new"] e.g for state {name,capital}, for others like lga, location and streets {name}

        if func.validate_input(json_data,"edit_record"):
            if json_data["what"] == "street":
                worker = STREET()
                response = worker.update_street_record(data_by_name=json_data["id"],new_record=json_data["new"])
                if response["status"] > 1:
                    error.append({"err_code":6,"data":json_data})
            elif json_data["what"] == "location":
                worker = LOCATION()
                response = worker.update_location_record(data_by_name=json_data["id"],new_record=json_data["new"])
                if response["status"] > 1:
                    error.append({"err_code":6,"data":json_data})
            elif json_data["what"] == "lga":
                worker = LGA()
                response = worker.update_lga_record(data_by_name=json_data["id"],new_record=json_data["new"])
                if response["status"] > 1:
                    error.append({"err_code":6,"data":json_data})
            elif json_data["what"] == "state":
                worker = STATE()
                response = worker.update_state_record(data_by_name=json_data["id"],new_record=json_data["new"])
                if response["status"] > 1:
                    error.append({"err_code":6,"data":json_data})                                    
        else:
            error.append({"err_code":4,"data":json_data})      

        if len(error) > 0:
            mr = {}
            mr["legend"] = func.error_legend()
            mr["errors"] = error
            status =  "error"            
        else:
            status = "success"
            mr = {}                                
        return json.dumps({"status":status,"error":mr})       



@app.route('/states/<state_name>')
def get_state(state_name):
    """ This route exposes information about a particular state in Nigeria when the state name is provided """
    error = []
    state_data = None

    look = STATE()
    response = look.get_state_info(state_name)

    if response["status"] == 1:
        status = "success"
        mr = {}
        state_data = response["data"]
    else:
        error.extend(response["error"])
        mr = {}
        mr["legend"] = func.error_legend()
        mr["errors"] = error
        status = "error"

    return json.dumps({"status":status,"data":state_data,"error":mr})    

if __name__ == "__name__":
    """ Main Function """    
    app.run()
