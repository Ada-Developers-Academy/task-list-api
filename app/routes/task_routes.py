from app import db
from app.models.task import Task
from flask import Blueprint, request, make_response, jsonify, abort

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# CREATE ONE TASK w/ POST REQUEST
@tasks_bp.route("", methods=['POST'])
def create_task():
    # use try / except to catch KeyError for invalid data
    try:
        # get post request data and convert to json
        request_body = request.get_json()

        # make a new instance of Task using request data
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"]
            )

        # add new task to database 
        db.session.add(new_task)
        db.session.commit()

        # return new task in json and successfully created status code
        return make_response(jsonify({"task": 
                    {"id": new_task.task_id,
                    "title": new_task.title,
                    "description": new_task.description,
                    "is_complete": new_task.is_complete
                    }}), 201)
    
    except KeyError:
        # abort and show error message if KeyError
        abort(make_response({"details": "Invalid data"}, 400))


# GET ALL TASKS w/ GET REQUEST
@tasks_bp.route("", methods=['GET'])
def get_all_tasks():
    # query all instances of Task
    tasks = Task.query.all()
    tasks_response = []

    # loop through all the instances of Task, add to response body
    # convert Task data into dictionary
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
        })
    
    # convert response into json and give successful status code
    return jsonify(tasks_response), 200


# GET ONE TASK w/ GET REQUEST
@tasks_bp.route("/<task_id>", methods=['GET'])
def get_one_task(task_id):
    # query one instance of Task given task_id
    task = Task.query.get(task_id)
    
    # return dictionary with Task data for one task
    return { "task": {
    "id": task.task_id,
    "title": task.title,
    "description": task.description,
    "is_complete": task.is_complete
    }}


# UPDATE ONE TASK w/ PUT REQUEST
@tasks_bp.route("/<task_id>", methods=['PUT'])
def update_task(task_id):
    # query one instance of Task given task_id
    task = Task.query.get(task_id)
    
    # get put request data and convert to json
    request_body = request.get_json()

    # update task attributes
    task.title = request_body["title"]
    task.description = request_body["description"]

    # update task in the database
    db.session.commit()

    # return updated task as a dictionary
    return { "task": {
    "id": task.task_id,
    "title": task.title,
    "description": task.description,
    "is_complete": task.is_complete
    }}