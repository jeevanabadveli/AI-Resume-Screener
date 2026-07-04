/* ==========================================================
   AI Resume Screener
   ranking.js
   Resume Ranking System
========================================================== */

"use strict";

/* ==========================================================
   INIT RANKING PAGE
========================================================== */

document.addEventListener("DOMContentLoaded", () => {

    if (window.location.pathname === "/ranking") {

        initializeRanking();

    }

});

/* ==========================================================
   INITIALIZE RANKING FORM
========================================================== */

function initializeRanking() {

    const form = document.getElementById("rankingForm");

    if (!form) return;

    form.addEventListener("submit", (e) => {

        e.preventDefault();

        rankResumes();

    });

}

/* ==========================================================
   RANK RESUMES API CALL
========================================================== */

async function rankResumes() {

    const jobInput = document.getElementById("job_description");

    const fileInput = document.getElementById("resumes");

    if (!jobInput || jobInput.value.trim() === "") {

        showToast("Job description is required", "error");

        return;

    }

    if (!fileInput || fileInput.files.length === 0) {

        showToast("Please upload resumes", "error");

        return;

    }

    const formData = new FormData();

    formData.append("job_description", jobInput.value.trim());

    for (let i = 0; i < fileInput.files.length; i++) {

        formData.append("resumes", fileInput.files[i]);

    }

    try {

        showLoader();

        const response = await fetch("/api/rank", {

            method: "POST",

            body: formData

        });

        const data = await response.json();

        hideLoader();

        if (!data.success) {

            showToast(data.message || "Ranking failed", "error");

            return;

        }

        renderRanking(data.ranked_resumes);

        showToast("Ranking completed ✔", "success");

    }

    catch (error) {

        hideLoader();

        console.error(error);

        showToast("Server error during ranking", "error");

    }

}

/* ==========================================================
   RENDER RANKING RESULTS
========================================================== */

function renderRanking(resumes) {

    const container = document.getElementById("rankingContainer");

    if (!container) return;

    container.innerHTML = "";

    if (!resumes || resumes.length === 0) {

        container.innerHTML = "<p>No resumes ranked.</p>";

        return;

    }

    resumes.forEach((resume, index) => {

        const card = document.createElement("div");

        card.className = "card ranking-card";

        card.innerHTML = `

            <div class="rank-badge">#${index + 1}</div>

            <h3>${resume.name}</h3>

            <div class="score-box">

                <p><strong>Match Score:</strong> ${resume.score}%</p>

            </div>

            <div class="progress-bar-container">

                <div class="progress-bar" style="width:${resume.score}%"></div>

            </div>

            ${index === 0 ? `<div class="top-candidate">🏆 Top Candidate</div>` : ""}

        `;

        container.appendChild(card);

    });

    animateRankingBars();

}

/* ==========================================================
   ANIMATE RANKING BARS
========================================================== */

function animateRankingBars() {

    const bars = document.querySelectorAll(".progress-bar");

    bars.forEach(bar => {

        const width = bar.style.width;

        bar.style.width = "0%";

        setTimeout(() => {

            bar.style.transition = "width 1s ease";

            bar.style.width = width;

        }, 200);

    });

}

/* ==========================================================
   REFRESH RANKING
========================================================== */

function refreshRanking() {

    rankResumes();

}

/* ==========================================================
   EXPORT GLOBAL FUNCTIONS
========================================================== */

window.rankResumes = rankResumes;

window.refreshRanking = refreshRanking;

/* ==========================================================
   END OF ranking.js
========================================================== */

console.log("ranking.js loaded ✔");