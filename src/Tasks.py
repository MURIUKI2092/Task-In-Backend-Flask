from flask import Blueprint

tasks=Blueprint("auth",__name__,url_prefix="/api/v1/tasks")

@tasks.post("/task")
def create_single_task():
    return "single task created"

@tasks.get("/task/<int>")
def get_single_task():
    return "This task was found"