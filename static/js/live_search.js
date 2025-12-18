document.addEventListener("DOMContentLoaded", function () {

    const input = document.querySelector(".search-input");

    if (!input) return;

    // Suggestion box
    const suggestionBox = document.createElement("div");
    suggestionBox.className = "search-suggestions";
    input.parentElement.appendChild(suggestionBox);

    input.addEventListener("keyup", function () {
        const query = this.value.trim();

        if (query.length < 2) {
            suggestionBox.innerHTML = "";
            suggestionBox.style.display = "none";
            return;
        }

        fetch(`/search-suggestions/?q=${query}`)
            .then(res => res.json())
            .then(data => {
                suggestionBox.innerHTML = "";

                if (data.length === 0) {
                    suggestionBox.style.display = "none";
                    return;
                }

                data.forEach(item => {
                    const div = document.createElement("div");
                    div.className = "suggestion-item";
                    div.innerText = item;

                    div.onclick = () => {
                        input.value = item;
                        suggestionBox.innerHTML = "";
                        suggestionBox.style.display = "none";
                    };

                    suggestionBox.appendChild(div);
                });

                suggestionBox.style.display = "block";
            });
    });

    document.addEventListener("click", () => {
        suggestionBox.style.display = "none";
    });
});
