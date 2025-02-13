document.getElementById("inputForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const functionStr = document.getElementById("function").value;
    const xRange = document.getElementById("range").value;
    const method = document.getElementById("numericalMethod").value;

    // Step 1: Get Graphical Method Graph
    let response = await fetch("/graphical-method", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ function: functionStr, x_range: xRange }),
    });
    document.getElementById("graphicalImage").src = URL.createObjectURL(await response.blob());

    // Step 2: Get Numerical Method Graph and Root
    response = await fetch("/numerical-method", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ function: functionStr, x_range: xRange, method }),
    });
    let data = await response.json();
    document.getElementById("numericalImage").src = data.image;
    const correctRoot = data.root;

    // Step 3: Calculate Absolute Error
    document.getElementById("approxRoot").addEventListener("input", async function () {
        let userRoot = document.getElementById("approxRoot").value;
        let errorResponse = await fetch("/calculate-error", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_root: userRoot, correct_root: correctRoot }),
        });

        let errorData = await errorResponse.json();
        document.getElementById("absoluteError").innerText = `Absolute Error: ${errorData.absolute_error}`;
    });
});