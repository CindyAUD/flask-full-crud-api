from flask import Flask, jsonify, request

app = Flask(__name__)

# Event class
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory data store
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Helper function to find an event by ID
def find_event(event_id):
    for event in events:
        if event.id == event_id:
            return event
    return None

# GET / - Welcome message
@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Welcome to the Event Management API"}), 200

# GET /events - Return all events
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200

# POST /events - Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    # Validate that title is provided
    if not data or "title" not in data or not data["title"]:
        return jsonify({"error": "Title is required"}), 400

    # Generate a new unique ID (simple increment)
    new_id = max(event.id for event in events) + 1 if events else 1
    new_event = Event(new_id, data["title"])
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201

# PATCH /events/<id> - Update the title of an event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json()
    if not data or "title" not in data or not data["title"]:
        return jsonify({"error": "Title is required"}), 400

    event.title = data["title"]
    return jsonify(event.to_dict()), 200

# DELETE /events/<id> - Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)
    return "", 204  # No Content

if __name__ == "__main__":
    app.run(debug=True)
    