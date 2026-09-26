async function startInvestigation() {

    const status = document.getElementById("aiStatus");

    status.innerHTML = "<span></span> AI Investigating...";
    status.style.color = "#d08b39";

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/api/investigate",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    scenario: "database_failure"
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Investigation failed");
        }

        console.log("Backend response:", data);

        status.innerHTML =
            "<span></span> Investigation Complete";

        status.style.color = "#159b8b";

        if (data.investigation) {

            document.getElementById("confidence").innerText =
                Math.round(data.investigation.confidence * 100) + "%";

            alert(
                "Root Cause: " +
                data.investigation.root_cause +
                "\n\nRecommended Action: " +
                data.investigation.recommended_action.type
            );
        }

    } catch (error) {

        console.error(error);

        status.innerHTML =
            "<span></span> Investigation Failed";

        status.style.color = "red";

        alert(
            "Backend connection failed: " +
            error.message
        );
    }
}


function simulateIncident() {

    document.getElementById(
        "activeIncidents"
    ).innerText = "02";

    alert(
        "Simulated incident created!\n\n" +
        "SentinelAI is correlating logs, metrics, " +
        "traces and deployment history."
    );
}


function approveAction(button) {

    button.innerText = "Approved";

    button.style.background = "#25a970";

    button.disabled = true;

    const action =
        button.parentElement;

    const title =
        action.querySelector("h3").innerText;

    console.log(
        "Approved remediation:",
        title
    );
}


setInterval(function () {

    const bars =
        document.querySelectorAll(
            ".metric-bar div"
        );

    bars.forEach(function (bar) {

        const value =
            65 + Math.random() * 30;

        bar.style.width =
            value + "%";

    });

}, 3000);


const navLinks =
    document.querySelectorAll("nav a");


navLinks.forEach(function (link) {

    link.addEventListener(
        "click",
        function () {

            navLinks.forEach(
                item =>
                    item.classList.remove("active")
            );

            link.classList.add("active");

        }
    );

});