document.addEventListener("DOMContentLoaded", () => {

    /* =====================================================
       CLIENT — DESCRIPTION COUNTER
    ====================================================== */

    const description = document.querySelector("#id_description");
    const counter = document.querySelector("#description-count");

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


    /* =====================================================
       CLIENT — PROJECT IDEAS
    ====================================================== */

    const ideaButtons =
        document.querySelectorAll(".project-idea");

    ideaButtons.forEach((button) => {

        button.addEventListener("click", () => {

            if (!description) {
                return;
            }

            const idea = button.dataset.idea;

            if (!idea) {
                return;
            }

            description.value = idea;

            description.dispatchEvent(
                new Event("input")
            );

            description.focus();
        });

    });


    /* =====================================================
       CLIENT — PROFILE EDIT
    ====================================================== */

    const editProfileButton =
        document.querySelector(
            "#edit-profile-button"
        );

    const cancelProfileButton =
        document.querySelector(
            "#cancel-profile-button"
        );

    const profileEditSection =
        document.querySelector(
            "#profile-edit-section"
        );


    if (
        editProfileButton &&
        cancelProfileButton &&
        profileEditSection
    ) {

        editProfileButton.addEventListener(
            "click",
            () => {

                profileEditSection.hidden = false;

                profileEditSection.scrollIntoView({
                    behavior: "smooth",
                    block: "start",
                });


                const firstInput =
                    profileEditSection.querySelector(
                        "input"
                    );


                if (firstInput) {
                    firstInput.focus();
                }

            }
        );


        cancelProfileButton.addEventListener(
            "click",
            () => {

                profileEditSection.hidden = true;

                editProfileButton.scrollIntoView({
                    behavior: "smooth",
                    block: "center",
                });

            }
        );

    }


    /* =====================================================
       ADMIN — DASHBOARD
    ====================================================== */

    const adminDashboard =
        document.querySelector(
            ".admin-dashboard"
        );


    if (!adminDashboard) {
        return;
    }


    const newCount =
        Number(
            adminDashboard.dataset.new || 0
        );

    const acceptedCount =
        Number(
            adminDashboard.dataset.accepted || 0
        );

    const completedCount =
        Number(
            adminDashboard.dataset.completed || 0
        );

    const rejectedCount =
        Number(
            adminDashboard.dataset.rejected || 0
        );


    const total =
        newCount +
        acceptedCount +
        completedCount +
        rejectedCount;


    /* =====================================================
       ADMIN — KPI COUNTER ANIMATION
    ====================================================== */

    const counters =
        adminDashboard.querySelectorAll(
            "[data-counter]"
        );


    counters.forEach((element) => {

        const target =
            Number(
                element.dataset.counter || 0
            );


        if (target === 0) {
            element.textContent = "0";
            return;
        }


        let current = 0;

        const duration = 650;

        const startTime =
            performance.now();


        const animateCounter = (time) => {

            const progress =
                Math.min(
                    (time - startTime) / duration,
                    1
                );


            const eased =
                1 -
                Math.pow(
                    1 - progress,
                    3
                );


            current =
                Math.round(
                    target * eased
                );


            element.textContent =
                current.toString();


            if (progress < 1) {

                requestAnimationFrame(
                    animateCounter
                );

            } else {

                element.textContent =
                    target.toString();

            }

        };


        requestAnimationFrame(
            animateCounter
        );

    });


    /* =====================================================
       ADMIN — DONUT CHART
    ====================================================== */

    const donut =
        document.querySelector(
            "#admin-donut"
        );


    const totalCount =
        document.querySelector(
            "#admin-total-count"
        );


    if (donut && totalCount) {

        totalCount.textContent =
            total.toString();


        if (total === 0) {

            donut.style.background =
                "conic-gradient(#272d3c 0deg 360deg)";

        } else {

            const newDegrees =
                (newCount / total) * 360;

            const acceptedDegrees =
                (acceptedCount / total) * 360;

            const completedDegrees =
                (completedCount / total) * 360;

            const rejectedDegrees =
                (rejectedCount / total) * 360;


            const first =
                newDegrees;

            const second =
                first + acceptedDegrees;

            const third =
                second + completedDegrees;

            const fourth =
                third + rejectedDegrees;


            donut.style.background =
                `conic-gradient(
                    #9274ff 0deg ${first}deg,
                    #55df9e ${first}deg ${second}deg,
                    #6fa1ff ${second}deg ${third}deg,
                    #ff7184 ${third}deg ${fourth}deg
                )`;

        }

    }


    /* =====================================================
       ADMIN — PIPELINE PROGRESS
    ====================================================== */

    const progressValues = {
        new: newCount,
        accepted: acceptedCount,
        completed: completedCount,
        rejected: rejectedCount,
    };


    const progressElements =
        adminDashboard.querySelectorAll(
            "[data-progress]"
        );


    progressElements.forEach((element) => {

        const key =
            element.dataset.progress;


        const value =
            progressValues[key] || 0;


        let percentage = 0;


        if (total > 0) {

            percentage =
                (value / total) * 100;

        }


        if (value > 0 && percentage < 8) {
            percentage = 8;
        }


        setTimeout(() => {

            element.style.width =
                `${percentage}%`;

        }, 120);

    });


    /* =====================================================
       ADMIN — ACTIVITY CHART
    ====================================================== */

    const activityChart =
        document.querySelector(
            "#admin-activity-chart"
        );


    if (activityChart) {

        const items =
            activityChart.querySelectorAll(
                ".admin-activity-item"
            );


        if (items.length > 0) {

            const dates = [];


            items.forEach((item) => {

                const value =
                    item.dataset.created;


                if (value) {
                    dates.push(value);
                }

            });


            const counts = {};


            dates.forEach((date) => {

                if (!counts[date]) {
                    counts[date] = 0;
                }

                counts[date] += 1;

            });


            let max =
                1;


            Object.values(counts).forEach(
                (value) => {

                    if (value > max) {
                        max = value;
                    }

                }
            );


            items.forEach((item, index) => {

                const date =
                    item.dataset.created;


                const value =
                    counts[date] || 0;


                let height =
                    (value / max) * 100;


                if (value === 0) {
                    height = 4;
                }


                if (height < 10) {
                    height = 10;
                }


                const bar =
                    item.querySelector(
                        ".admin-activity-bar"
                    );


                if (!bar) {
                    return;
                }


                bar.style.height = "4%";


                setTimeout(() => {

                    bar.style.height =
                        `${height}%`;

                }, 120 + index * 70);

            });

        }

    }


    /* =====================================================
       ADMIN — LEGEND VALUES
    ====================================================== */

    const statusValues = {
        new: newCount,
        accepted: acceptedCount,
        completed: completedCount,
        rejected: rejectedCount,
    };


    const statusElements =
        adminDashboard.querySelectorAll(
            "[data-status-value]"
        );


    statusElements.forEach((element) => {

        const key =
            element.dataset.statusValue;


        if (
            Object.prototype.hasOwnProperty.call(
                statusValues,
                key
            )
        ) {

            element.textContent =
                statusValues[key].toString();

        }

    });

});
