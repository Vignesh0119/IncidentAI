# incident_engine.py

class IncidentEngine:

    def __init__(self, incident):
        self.incident = incident

    def investigate(self):

        logs = self.incident["logs"]
        metrics = self.incident["metrics"]
        deployments = self.incident["deployments"]

        hypotheses = []

        # -----------------------------------------
        # 1. DATABASE FAILURE
        # -----------------------------------------
        if (
            metrics.get("db_connections", 0) >= 90
            or any("database connection" in log.lower() for log in logs)
            or any("connection pool" in log.lower() for log in logs)
        ):
            hypotheses.append({
                "cause": "Database connection pool exhaustion",
                "score": 0.90
            })

        # -----------------------------------------
        # 2. BAD DEPLOYMENT
        # -----------------------------------------
        if (
            any("exception" in log.lower() for log in logs)
            or any("500" in log for log in logs)
            or any("deployment" in log.lower() for log in logs)
        ):
            hypotheses.append({
                "cause": "Bad deployment",
                "score": 0.85
            })

        # -----------------------------------------
        # 3. PAYMENT FAILURE
        # -----------------------------------------
        if (
            any("payment gateway" in log.lower() for log in logs)
            or metrics.get("gateway_errors", 0) > 50
        ):
            hypotheses.append({
                "cause": "Payment gateway failure",
                "score": 0.92
            })

        # -----------------------------------------
        # 4. NETWORK LATENCY
        # -----------------------------------------
        if metrics.get("network_latency_ms", 0) > 1000:
            hypotheses.append({
                "cause": "Network latency",
                "score": 0.88
            })

        # -----------------------------------------
        # 5. HIGH CPU
        # -----------------------------------------
        if metrics.get("cpu_usage", 0) >= 90:
            hypotheses.append({
                "cause": "High CPU usage",
                "score": 0.91
            })

        # If nothing matched
        if not hypotheses:
            hypotheses.append({
                "cause": "Unknown",
                "score": 0.30
            })

        # Sort highest score first
        hypotheses.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        # Select highest scoring hypothesis
        best = hypotheses[0]

        # -----------------------------------------
        # COLLECT EVIDENCE
        # -----------------------------------------

        evidence = []

        for log in logs:
            if any(
                word in log.lower()
                for word in [
                    "timeout",
                    "exhausted",
                    "failed",
                    "error",
                    "exception",
                    "latency",
                    "cpu",
                    "gateway"
                ]
            ):
                evidence.append(log)

        # Add important metrics
        if metrics.get("cpu_usage", 0) >= 90:
            evidence.append(
                f"CPU usage reached {metrics['cpu_usage']}%"
            )

        if metrics.get("db_connections", 0) >= 90:
            evidence.append(
                f"Database connections reached "
                f"{metrics['db_connections']}%"
            )

        if metrics.get("network_latency_ms", 0) > 1000:
            evidence.append(
                f"Network latency reached "
                f"{metrics['network_latency_ms']} ms"
            )

        # -----------------------------------------
        # RECOMMENDED ACTION
        # -----------------------------------------

        service = self.incident["service"]

        if best["cause"] == "Database connection pool exhaustion":

            action = {
                "type": "rollback",
                "service": service,
                "from_version": deployments[0]["version"],
                "to_version": "1.4"
            }

        elif best["cause"] == "Bad deployment":

            previous = deployments[0].get(
                "previous_version",
                "previous version"
            )

            action = {
                "type": "rollback",
                "service": service,
                "from_version": deployments[0]["version"],
                "to_version": previous
            }

        elif best["cause"] == "Payment gateway failure":

            action = {
                "type": "restart_service",
                "service": service
            }

        elif best["cause"] == "Network latency":

            action = {
                "type": "network_check",
                "service": service
            }

        elif best["cause"] == "High CPU usage":

            action = {
                "type": "scale_service",
                "service": service
            }

        else:

            action = {
                "type": "manual_investigation",
                "service": service
            }

        # -----------------------------------------
        # FINAL RESULT
        # -----------------------------------------

        return {
            "root_cause": best["cause"],
            "confidence": best["score"],
            "evidence": evidence[:5],
            "hypotheses": hypotheses,
            "recommended_action": action
        }


# -----------------------------------------
# TEST
# -----------------------------------------

if __name__ == "__main__":

    from Scenarios import SCENARIOS

    incident = SCENARIOS["database_failure"]

    engine = IncidentEngine(incident)

    result = engine.investigate()

    print("\nROOT CAUSE:")
    print(result["root_cause"])

    print("\nCONFIDENCE:")
    print(result["confidence"])

    print("\nEVIDENCE:")

    for item in result["evidence"]:
        print("-", item)

    print("\nHYPOTHESES:")

    for hypothesis in result["hypotheses"]:
        print(
            "-",
            hypothesis["cause"],
            "=>",
            hypothesis["score"]
        )

    print("\nRECOMMENDED ACTION:")
    print(result["recommended_action"])