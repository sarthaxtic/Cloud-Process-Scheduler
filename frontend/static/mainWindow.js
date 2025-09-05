document.addEventListener("DOMContentLoaded", function () {
    const BASE_URL = "http://localhost:5000"; // Flask server address

    const exitBtn = document.getElementById("exit");
    const nextBtn = document.getElementById("next");
    const predictBtn = document.getElementById("predict");
    const algoTypes = document.querySelectorAll('input[name="main-question"]');

    // Enable Next button only when an algorithm is selected
    algoTypes.forEach(type => {
        type.addEventListener('change', () => {
            nextBtn.disabled = false;
        });
    });

    // Handle Exit button click
    exitBtn.addEventListener("click", function () {
        window.location.href = `${BASE_URL}/exit`;
    });

    // Handle Predict button click
    predictBtn.addEventListener("click", function () {
        window.location.href = `${BASE_URL}/predict`;
    });

    // Handle Next button click
    nextBtn.addEventListener("click", function () {
        let schedulerType = null;
        for (let algoType of algoTypes) {
            if (algoType.checked) {
                schedulerType = algoType.value;
                break;
            }
        }

        if (schedulerType) {
            window.location.href = `${BASE_URL}/algorithm?selected=${schedulerType}`;
        } else {
            alert("Please select a scheduling algorithm before continuing.");
        }
    });
});
