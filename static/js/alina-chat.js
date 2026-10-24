document.addEventListener("DOMContentLoaded", () => {
    const chat = document.getElementById("alina-chat");

    if (!chat) return;

    const launcher = document.getElementById("alina-chat-launcher");
    const panel = document.getElementById("alina-chat-panel");
    const closeButton = document.getElementById("alina-chat-close");
    const messages = document.getElementById("alina-chat-messages");
    const suggestions = document.getElementById("alina-chat-suggestions");

    if (!launcher || !panel || !closeButton || !messages || !suggestions) {
        return;
    }

    const questions = [

        {
            label: "Help me come up with a project idea",
            answer:
                "Let's brainstorm! Think about a problem you'd like to solve. " +
                "For example, we could explore a website for a small business, " +
                "a Telegram bot for automation, a personal finance tracker, " +
                "or a travel planning app. Tell me what interests you, and " +
                "I'll help you develop the idea. For a full conversation, " +
                "you can discuss your idea with Oleg."
        },
        {
            label: "Help me choose a project name",
            answer:
                "Of course! A good project name should be memorable, easy to " +
                "pronounce, and relevant to what the project does. Tell me " +
                "what your project will do, who it is for, and what style you " +
                "prefer — professional, creative, or playful. I can help you " +
                "brainstorm name options. Remember to check domain and trademark availability."
        },
        {
            label: "Help me plan an app or website",
            answer:
                "Let's turn your idea into a plan! Start by describing the " +
                "problem your app or website will solve and who will use it. " +
                "Then we can outline the core features, choose suitable " +
                "technologies, and define a simple first version (MVP). " +
                "For a tailored development plan, you can contact Oleg."
        },
        {
            label: "What Python project could I build?",
            answer:
                "Python is useful for APIs, web applications, Telegram bots, " +
                "automation and data processing. A few starter ideas are a " +
                "task tracker API, a booking system, a Telegram reminder bot, " +
                "or a personal expense tracker. Tell me your experience level " +
                "and interests, and I can suggest a suitable project."
        },

        {
            label: "Who is Oleg?",
            answer:
                "Oleg is a Junior Python Backend Developer and the creator " +
                "of OlehDev. He focuses on Python, backend development, " +
                "web applications and APIs."
        },
        {
            label: "What projects has he built?",
            answer:
                "Oleg's portfolio features work related to web applications, " +
                "REST APIs, backend services and Telegram bots. Visit the " +
                "Portfolio section to explore the projects presented on this website."
        },
        {
            label: "Which technologies does he use?",
            answer:
                "Oleg works with Python, Django, FastAPI, REST APIs, SQL, " +
                "PostgreSQL, Docker and Git. The technologies used depend " +
                "on the project."
        },
        {
            label: "Where can I find his GitHub and live projects?",
            answer:
                "Yes! Oleg has a GitHub profile. You can explore his repositories " +
                "and code at github.com/o7111023-pixel.\n\n" +
                "You can also visit the Portfolio page on OlehDev to explore his projects. " +
                "Each project may include a GitHub link and, when the project is deployed, " +
                "a live demo link so you can try it yourself."
        },
        {
            label: "Does he build Telegram bots?",
            answer:
                "Yes! Oleg has practical experience with Python development " +
                "and is interested in building Telegram bots and automation tools. " +
                "Contact him to discuss your requirements."
        },
        {
            label: "Can he build a website or an API?",
            answer:
                "Yes! Oleg has practical experience in Python development and " +
                "works with backend technologies, web applications and APIs. " +
                "Tell him about your idea so you can discuss the requirements " +
                "and determine the best approach."
        },
        {
            label: "Where did he study programming?",
            answer:
                "Oleg studies programming through Mate Academy, following the " +
                "Python Developer course. He is developing his skills through " +
                "practical exercises, projects and independent learning. " +
                "His current professional level is Junior."
        },
        {
            label: "Does he have practical experience?",
            answer:
                "Yes! Oleg has practical experience working on Python projects, " +
                "including backend development, APIs, databases and application " +
                "features. He continues to strengthen his skills by building " +
                "projects and solving real development tasks."
        },
        {
            label: "What does development cost?",
            answer:
                "The price depends on the complexity, features and deadlines. " +
                "Contact Oleg with a description of your idea to discuss " +
                "the scope of work and possible budget."
        },
        {
            label: "What does he enjoy outside programming?",
            answer:
                "Oleg lives in Germany and loves travelling. He has visited " +
                "more than 11 countries and enjoys discovering new places, " +
                "cultures and experiences."
        },
        {
            label: "Can I discuss my own idea with him?",
            answer:
                "Absolutely! Oleg welcomes ideas for websites, APIs, Telegram " +
                "bots and automation tools. Contact him directly to discuss " +
                "your goals, requirements and possible implementation."
        },
        {
            label: "How can I contact Oleg?",
            answer:
                "You can contact Oleg directly through Telegram using the " +
                "'Discuss a project with Oleg' button below. Tell him about " +
                "your idea and what you want to achieve."
        }
    ];

    function openChat() {
        panel.hidden = false;
        panel.setAttribute("aria-hidden", "false");
        launcher.setAttribute("aria-expanded", "true");
    }

    function closeChat() {
        panel.hidden = true;
        panel.setAttribute("aria-hidden", "true");
        launcher.setAttribute("aria-expanded", "false");
        launcher.focus();
    }

    function scrollToBottom() {
        messages.scrollTop = messages.scrollHeight;
    }

    function addMessage(text, type) {
        const article = document.createElement("article");
        article.className = `alina-message alina-message--${type}`;

        const paragraph = document.createElement("p");
        paragraph.textContent = text;

        article.appendChild(paragraph);
        messages.insertBefore(article, suggestions);

        scrollToBottom();
    }

    function showQuestions() {
        suggestions.replaceChildren();

        const toggle = document.createElement("button");
        toggle.type = "button";
        toggle.className = "alina-chat__questions-toggle";
        toggle.textContent = "Questions · " + questions.length;
        toggle.setAttribute("aria-expanded", "false");

        const list = document.createElement("div");
        list.className = "alina-chat__question-list";
        list.hidden = true;

        questions.forEach((item, index) => {
            const button = document.createElement("button");

            button.type = "button";
            button.className = "alina-chat__question";
            button.textContent = `${index + 1}. ${item.label}`;
            button.dataset.questionIndex = index;

            list.appendChild(button);
        });

        toggle.addEventListener("click", () => {
            const isOpening = list.hidden;

            list.hidden = !isOpening;
            toggle.setAttribute("aria-expanded", String(isOpening));
            toggle.textContent = isOpening
                ? "Hide questions"
                : "Questions · " + questions.length;

            if (isOpening) {
                scrollToBottom();
            }
        });

        suggestions.appendChild(toggle);
        suggestions.appendChild(list);
        suggestions.hidden = false;
    }

    function answerQuestion(index) {
        const item = questions[index];

        if (!item) return;

        addMessage(item.label, "user");
        suggestions.hidden = true;

        window.setTimeout(() => {
            addMessage(item.answer, "assistant");
            showQuestions();
            scrollToBottom();
        }, 200);
    }

    launcher.addEventListener("click", () => {
        if (panel.hidden) {
            openChat();
        } else {
            closeChat();
        }
    });

    closeButton.addEventListener("click", closeChat);

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && !panel.hidden) {
            closeChat();
        }
    });

    suggestions.addEventListener("click", (event) => {
        const button = event.target.closest("[data-question-index]");

        if (!button) return;

        answerQuestion(Number(button.dataset.questionIndex));
    });

    showQuestions();
});
