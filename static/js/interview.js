/* ==========================================================
   AI Resume Screener
   interview.js
   Interview Question Generator UI
========================================================== */

"use strict";

/* ==========================================================
   INITIALIZE INTERVIEW PAGE
========================================================== */

document.addEventListener("DOMContentLoaded", () => {

    if (window.location.pathname === "/interview") {

        initializeInterview();

    }

});

/* ==========================================================
   MAIN INITIALIZER
========================================================== */

async function initializeInterview() {

    await loadInterviewQuestions();

}

/* ==========================================================
   LOAD INTERVIEW QUESTIONS FROM BACKEND
========================================================== */

async function loadInterviewQuestions() {

    try {

        const latest = loadLocal("latestResult");

        if (!latest) {

            showToast("No resume data found. Please analyze a resume first.", "error");

            return;

        }

        const payload = {

            skills: latest.skills || [],

            education: latest.education || [],

            job_description: latest.job_description || ""

        };

        const response = await fetch("/api/interview", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify(payload)

        });

        const data = await response.json();

        if (!data.success) {

            showToast(data.message || "Failed to load questions", "error");

            return;

        }

        renderInterviewQuestions(data.questions);

        console.log("Interview loaded ✔");

    }

    catch (error) {

        console.error("Interview Error:", error);

        showToast("Error loading interview questions", "error");

    }

}

/* ==========================================================
   RENDER QUESTIONS
========================================================== */

function renderInterviewQuestions(questions) {

    const container = document.getElementById("interviewContainer");

    if (!container) return;

    container.innerHTML = "";

    if (!questions || questions.length === 0) {

        container.innerHTML = "<p>No questions generated.</p>";

        return;

    }

    questions.forEach((q, index) => {

        const card = document.createElement("div");

        card.className = "card interview-card";

        card.innerHTML = `

            <div class="question-number">Q${index + 1}</div>

            <div class="question-text">${q}</div>

            <button class="btn btn-primary" onclick="toggleAnswer(this)">

                Show Hint

            </button>

            <div class="answer-box hidden">

                <p>Think about real-world experience, tools, and problem-solving approach.</p>

            </div>

        `;

        container.appendChild(card);

    });

}

/* ==========================================================
   TOGGLE ANSWER/HINT
========================================================== */

function toggleAnswer(btn) {

    const answerBox = btn.nextElementSibling;

    if (!answerBox) return;

    answerBox.classList.toggle("hidden");

    btn.textContent = answerBox.classList.contains("hidden")

        ? "Show Hint"

        : "Hide Hint";

}

/* ==========================================================
   REFRESH INTERVIEW QUESTIONS
========================================================== */

async function refreshInterview() {

    showToast("Refreshing interview questions...", "success");

    await loadInterviewQuestions();

}

/* ==========================================================
   EXPORT GLOBAL FUNCTIONS
========================================================== */

window.initializeInterview = initializeInterview;

window.loadInterviewQuestions = loadInterviewQuestions;

window.toggleAnswer = toggleAnswer;

window.refreshInterview = refreshInterview;

/* ==========================================================
   END OF interview.js
========================================================== */

console.log("interview.js loaded ✔");