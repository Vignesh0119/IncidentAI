# scenarios.py

SCENARIOS = {

    # -------------------------------------------------
    # SCENARIO 1: DATABASE CONNECTION FAILURE
    # -------------------------------------------------
    "database_failure": {

        "incident_id": "INC-001",
        "service": "order-service",
        "severity": "HIGH",

        "logs": [
            "Database connection timeout",
            "Connection pool exhausted",
            "Order request failed",
            "Failed to acquire database connection"
        ],

        "metrics": {
            "error_rate": 35,
            "cpu_usage": 72,
            "db_connections": 100,
            "response_time_ms": 2400
        },

        "traces": [
            "order-service -> database: timeout",
            "database connection acquisition: failed",
            "order-service -> database: connection refused"
        ],

        "deployments": [
            {
                "service": "order-service",
                "version": "1.5",
                "time": "10:00"
            }
        ],

        "dependencies": [
            "order-service -> database",
            "order-service -> payment-service"
        ]
    },


    # -------------------------------------------------
    # SCENARIO 2: BAD DEPLOYMENT
    # -------------------------------------------------
    "bad_deployment": {

        "incident_id": "INC-002",
        "service": "user-service",
        "severity": "HIGH",

        "logs": [
            "Application error after deployment",
            "NullPointerException in user-service",
            "User request failed",
            "500 Internal Server Error"
        ],

        "metrics": {
            "error_rate": 48,
            "cpu_usage": 65,
            "memory_usage": 82,
            "response_time_ms": 1800
        },

        "traces": [
            "frontend -> user-service: HTTP 500",
            "user-service -> database: successful",
            "user-service: application exception"
        ],

        "deployments": [
            {
                "service": "user-service",
                "version": "2.4",
                "previous_version": "2.3",
                "time": "11:20"
            }
        ],

        "dependencies": [
            "frontend -> user-service",
            "user-service -> database",
            "user-service -> auth-service"
        ]
    },


    # -------------------------------------------------
    # SCENARIO 3: PAYMENT SERVICE FAILURE
    # -------------------------------------------------
    "payment_failure": {

        "incident_id": "INC-003",
        "service": "payment-service",
        "severity": "CRITICAL",

        "logs": [
            "Payment gateway request failed",
            "Payment service timeout",
            "Transaction processing failed",
            "External gateway unavailable"
        ],

        "metrics": {
            "error_rate": 65,
            "cpu_usage": 78,
            "gateway_errors": 92,
            "response_time_ms": 4200
        },

        "traces": [
            "order-service -> payment-service: timeout",
            "payment-service -> payment-gateway: failed",
            "payment-gateway: connection timeout"
        ],

        "deployments": [
            {
                "service": "payment-service",
                "version": "3.1",
                "time": "12:10"
            }
        ],

        "dependencies": [
            "order-service -> payment-service",
            "payment-service -> payment-gateway",
            "payment-service -> database"
        ]
    },


    # -------------------------------------------------
    # SCENARIO 4: NETWORK LATENCY
    # -------------------------------------------------
    "network_latency": {

        "incident_id": "INC-004",
        "service": "api-gateway",
        "severity": "MEDIUM",

        "logs": [
            "Upstream request taking too long",
            "Network timeout warning",
            "Slow response from order-service",
            "Request latency threshold exceeded"
        ],

        "metrics": {
            "error_rate": 12,
            "cpu_usage": 55,
            "network_latency_ms": 1800,
            "response_time_ms": 3200
        },

        "traces": [
            "client -> api-gateway: 3200ms",
            "api-gateway -> order-service: 1800ms",
            "order-service -> database: 200ms"
        ],

        "deployments": [
            {
                "service": "api-gateway",
                "version": "1.8",
                "time": "13:30"
            }
        ],

        "dependencies": [
            "client -> api-gateway",
            "api-gateway -> order-service",
            "order-service -> database"
        ]
    },


    # -------------------------------------------------
    # SCENARIO 5: HIGH CPU USAGE
    # -------------------------------------------------
    "high_cpu": {

        "incident_id": "INC-005",
        "service": "analytics-service",
        "severity": "HIGH",

        "logs": [
            "CPU usage above threshold",
            "Worker processing queue slowly",
            "Request processing delayed",
            "Service performance degraded"
        ],

        "metrics": {
            "error_rate": 18,
            "cpu_usage": 98,
            "memory_usage": 76,
            "response_time_ms": 2800
        },

        "traces": [
            "frontend -> analytics-service: slow response",
            "analytics-service -> database: normal",
            "analytics-service -> worker: processing delay"
        ],

        "deployments": [
            {
                "service": "analytics-service",
                "version": "4.2",
                "time": "14:15"
            }
        ],

        "dependencies": [
            "frontend -> analytics-service",
            "analytics-service -> database",
            "analytics-service -> worker"
        ]
    }
}


# -------------------------------------------------
# TEST THE SCENARIOS
# -------------------------------------------------

if __name__ == "__main__":

    import json

    print("Available Incident Scenarios:")
    
    for name in SCENARIOS:
        print("-", name)

    print("\nTesting database_failure scenario:\n")

    print(
        json.dumps(
            SCENARIOS["database_failure"],
            indent=2
        )
    )