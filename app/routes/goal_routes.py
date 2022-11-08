from app import db
from app.models.goal import Goal
from flask import Blueprint, request, make_response, jsonify, abort
from app.routes.route_helpers import validate_model

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

#Get all goals - GET 
@goals_bp.route("", methods = ["GET"])
def get_goals():
    goals = Goal.query.all()
    goals_response = [] 

    for goal in goals:
        goals_response.append(goal.to_dict())

    return jsonify(goals_response)


#CReate a goal - POST
@goals_bp.route("", methods=['POST'])
def create_goal():
    try:
       
        request_body = request.get_json()
        new_goal = Goal(title = request_body["title"])

        db.session.add(new_goal)
        db.session.commit()

        return {
        "goal": new_goal.to_dict()
   }, 201

    except KeyError:
        
        abort(make_response({"details": "Invalid data"}, 400))


#validate goals
def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except: 
        abort(make_response({"message": f"{goal_id} is invalid"}, 400))

    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"message": f"Goal {goal_id} not found"}, 404))

    return goal


#Get a goal - GET 
@goals_bp.route("/<goal_id>", methods=['GET'])
def get_one_goal(goal_id):
    #call helper function to validate the task_id
    goal = validate_goal(goal_id)
    
    # return dictionary with goal data
    return {"goal": goal.to_dict()}

#Update a goal - put
@goals_bp.route("/<goal_id>", methods=['PUT'])
def update_goal(goal_id):
    #validate goal using helper function
    goal = validate_goal(goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.add(goal)
    db.session.commit()
    
    # return dictionary with goal data
    return {"goal": goal.to_dict()}

#Delete a goal - delete
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
   #validate goal using helper function
   goal = validate_goal(goal_id)

   db.session.delete(goal)
   db.session.commit()
   
   return make_response({"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"})
