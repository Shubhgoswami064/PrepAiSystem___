function startQuiz() {
    const subject = document.getElementById("subject").value;
    const difficulty = document.getElementById("difficulty").value;

    fetch("/start_quiz", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            subject: subject,
            difficulty: difficulty
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);

        // future redirect to quiz page
        alert("Quiz Started!");
    });
}

function logout() {
    fetch("/logout")
    .then(() => {
        window.location.href = "/";
    });
}