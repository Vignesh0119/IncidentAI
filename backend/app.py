from flask import Flask, jsonify, request
from flask_cors import CORS

from Scenarios import SCENARIOS
from incident_engine import IncidentEngine
from remediation import (
    create_remediation,
    approve_remediation,
    execute_remediation,
    verify_remediation
)

app = Flask(__name__)
CORS(app)


@app.route("/api/scenarios", methods=["GET"])
def get_scenarios():
    return jsonify(list(SCENARIOS.keys()))


@app.route("/api/investigate", methods=["POST"])
def investigate():

    data = request.json
    scenario_name = data.get("scenario")

    if scenario_name not in SCENARIOS:
        return jsonify({"error": "Scenario not found"}), 404

    incident = SCENARIOS[scenario_name]

    engine = IncidentEngine(incident)
    result = engine.investigate()

    remediation = create_remediation(result)

    return jsonify({
        "incident": incident,
        "investigation": result,
        "remediation": remediation
    })


@app.route("/api/remediate", methods=["POST"])
def remediate():

    data = request.json
    action = data.get("action")

    remediation = {
        "status": "PENDING_APPROVAL",
        "action": action,
        "message": "Human approval required before execution."
    }

    approve_remediation(remediation)

    execution = execute_remediation(remediation)
    verification = verify_remediation(execution)

    return jsonify({
        "remediation": remediation,
        "execution": execution,
        "verification": verification
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)