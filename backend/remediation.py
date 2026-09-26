# remediation.py

from audit import write_audit


def create_remediation(investigation_result):
    """
    Create a safe remediation plan from the AI investigation result.
    """

    action = investigation_result["recommended_action"]

    return {
        "status": "PENDING_APPROVAL",
        "action": action,
        "message": "Human approval required before execution."
    }


def approve_remediation(remediation):
    """
    Simulate human approval.
    """

    remediation["status"] = "APPROVED"

    write_audit(
        "HUMAN_APPROVAL",
        {
            "status": "approved",
            "action": remediation["action"]
        }
    )

    return remediation


def reject_remediation(remediation):
    """
    Reject the recommended action.
    """

    remediation["status"] = "REJECTED"

    write_audit(
        "HUMAN_REJECTION",
        {
            "status": "rejected",
            "action": remediation["action"]
        }
    )

    return remediation


def execute_remediation(remediation):
    """
    Simulate remediation in a sandbox.
    No real production system is changed.
    """

    if remediation["status"] != "APPROVED":
        return {
            "status": "BLOCKED",
            "message": "Remediation requires human approval."
        }

    action = remediation["action"]

    write_audit(
        "SANDBOX_EXECUTION_STARTED",
        action
    )

    # Simulated execution
    result = {
        "status": "SUCCESS",
        "message": "Remediation successfully simulated in sandbox.",
        "action": action
    }

    write_audit(
        "SANDBOX_EXECUTION_COMPLETED",
        result
    )

    remediation["status"] = "EXECUTED"

    return result


def verify_remediation(execution_result):
    """
    Simulate verification after remediation.
    """

    if execution_result["status"] != "SUCCESS":
        return {
            "status": "FAILED",
            "message": "Remediation verification failed."
        }

    verification = {
        "status": "VERIFIED",
        "error_rate": "Reduced",
        "response_time": "Improved",
        "message": "System health verified after remediation."
    }

    write_audit(
        "VERIFICATION",
        verification
    )

    return verification


def rollback(remediation):
    """
    Simulate rollback if remediation causes a problem.
    """

    action = remediation["action"]

    rollback_result = {
        "status": "ROLLED_BACK",
        "message": "Simulated rollback completed.",
        "original_action": action
    }

    write_audit(
        "ROLLBACK",
        rollback_result
    )

    return rollback_result