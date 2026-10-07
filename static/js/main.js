document.addEventListener("DOMContentLoaded", () => {

    const description = document.querySelector(
        "#id_description"
    );

    const counter = document.querySelector(
        "#description-count"
    );

    if (description && counter) {

        const updateCounter = () => {
            counter.textContent = description.value.length;
        };

        updateCounter();

        description.addEventListener(
            "input",
            updateCounter
        );
    }


    const ideaButtons = document.querySelectorAll(
        ".project-idea"
    );

    ideaButtons.forEach((button) => {

        button.addEventListener("click", () => {

            if (!description) {
                return;
            }

            const idea = button.dataset.idea;

            description.value = idea;

            description.dispatchEvent(
                new Event("input")
            );

            description.focus();

        });

    });

});
