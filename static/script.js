function getRecommendations() {
    const movieName = document.getElementById("movieInput").value;
    const resultsList = document.getElementById("results");
    const loading = document.getElementById("loading");

    resultsList.innerHTML = "";
    loading.classList.remove("hidden");

    fetch("/recommend", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ movie_name: movieName })
    })
    .then(response => response.json())
    .then(data => {
        loading.classList.add("hidden");

        if (data.length === 0) {
            resultsList.innerHTML = "<li>Movie not found 😢</li>";
            return;
        }

        data.forEach(movie => {
            const li = document.createElement("li");
            li.textContent = movie;
            resultsList.appendChild(li);
        });
    })
    .catch(error => {
        loading.classList.add("hidden");
        resultsList.innerHTML = "<li>Error occurred. Try again.</li>";
    });
}
