/* ==========================================================
   AI Resume Screener
   Main JavaScript File
   Compatible with existing Flask Backend
========================================================== */

"use strict";

/* ==========================================================
   Global Variables
========================================================== */

const API = {

    analyze: "/api/analyze",

    dashboard: "/api/dashboard",

    analytics: "/api/analytics",

    history: "/api/history",

    result: "/api/result",

    rank: "/api/rank",

    interview: "/api/interview",

    downloadReport: "/api/download-report",

    health: "/api/health"

};

let latestResult = null;

let dashboardData = null;

let charts = {};

let darkMode = false;

/* ==========================================================
   DOM Ready
========================================================== */

document.addEventListener("DOMContentLoaded", () => {

    initializeApplication();

});

/* ==========================================================
   Initialize Application
========================================================== */

function initializeApplication() {

    hideLoader();

    initializeTheme();

    initializeNavigation();

    initializeButtons();

    initializeTooltips();

    initializeUpload();

    initializePage();

}

/* ==========================================================
   Detect Current Page
========================================================== */

function initializePage() {

    const path = window.location.pathname;

    switch (path) {

        case "/":

            console.log("Home Page Loaded");

            break;

        case "/dashboard":

            if (typeof loadDashboard === "function")
                loadDashboard();

            break;

        case "/history":

            if (typeof loadHistory === "function")
                loadHistory();

            break;

        case "/report":

            if (typeof loadLatestReport === "function")
                loadLatestReport();

            break;

        default:

            break;

    }

}

/* ==========================================================
   API Helper
========================================================== */

async function apiRequest(url, options = {}) {

    try {

        showLoader();

        const response = await fetch(url, options);

        const data = await response.json();

        hideLoader();

        return data;

    }

    catch (error) {

        hideLoader();

        showToast(error.message, "error");

        console.error(error);

        return null;

    }

}

/* ==========================================================
   Loader
========================================================== */

function showLoader() {

    const loader = document.getElementById("loader");

    if (loader)

        loader.classList.remove("hidden");

}

function hideLoader() {

    const loader = document.getElementById("loader");

    if (loader)

        loader.classList.add("hidden");

}

/* ==========================================================
   Toast Notification
========================================================== */

function showToast(message, type = "success") {

    let toast = document.createElement("div");

    toast.className = `toast ${type}`;

    toast.innerHTML = message;

    document.body.appendChild(toast);

    setTimeout(() => {

        toast.classList.add("show");

    }, 100);

    setTimeout(() => {

        toast.classList.remove("show");

        setTimeout(() => {

            toast.remove();

        }, 400);

    }, 3500);

}

/* ==========================================================
   Theme
========================================================== */

function initializeTheme() {

    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "dark") {

        darkMode = true;

        document.body.classList.add("dark");

    }

}

function toggleTheme() {

    darkMode = !darkMode;

    document.body.classList.toggle("dark");

    localStorage.setItem(

        "theme",

        darkMode ? "dark" : "light"

    );

}

/* ==========================================================
   Navigation
========================================================== */

function initializeNavigation() {

    const links = document.querySelectorAll(".sidebar a");

    links.forEach(link => {

        if (window.location.pathname === link.getAttribute("href")) {

            link.classList.add("active");

        }

    });

}

/* ==========================================================
   Buttons
========================================================== */

function initializeButtons() {

    document.querySelectorAll("button").forEach(btn => {

        btn.addEventListener("click", () => {

            btn.classList.add("clicked");

            setTimeout(() => {

                btn.classList.remove("clicked");

            }, 250);

        });

    });

}

/* ==========================================================
   Tooltips
========================================================== */

function initializeTooltips() {

    document.querySelectorAll("[data-tooltip]").forEach(item => {

        item.addEventListener("mouseenter", () => {

            item.classList.add("tooltip-show");

        });

        item.addEventListener("mouseleave", () => {

            item.classList.remove("tooltip-show");

        });

    });

}

/* ==========================================================
   Utility Functions
========================================================== */

function formatPercentage(value) {

    return `${Number(value).toFixed(0)}%`;

}

function formatDate(dateString) {

    if (!dateString)

        return "--";

    return new Date(dateString)

        .toLocaleString();

}

function clearElement(id) {

    const el = document.getElementById(id);

    if (el)

        el.innerHTML = "";

}

function setText(id, value) {

    const el = document.getElementById(id);

    if (el)

        el.textContent = value;

}

function setHTML(id, value) {

    const el = document.getElementById(id);

    if (el)

        el.innerHTML = value;

}

function createBadge(text, type = "primary") {

    return `<span class="badge badge-${type}">${text}</span>`;

}

/* ==========================================================
   Progress Bars
========================================================== */

function updateProgress(id, value) {

    const bar = document.getElementById(id);

    if (!bar)

        return;

    bar.style.width = value + "%";

    bar.innerHTML = value + "%";

}

/* ==========================================================
   Number Animation
========================================================== */

function animateValue(id, endValue) {

    const el = document.getElementById(id);

    if (!el)

        return;

    let current = 0;

    const step = Math.ceil(endValue / 50);

    const timer = setInterval(() => {

        current += step;

        if (current >= endValue) {

            current = endValue;

            clearInterval(timer);

        }

        el.innerHTML = current;

    }, 20);

}

/* ==========================================================
   Local Storage
========================================================== */

function saveLocal(key, value) {

    localStorage.setItem(

        key,

        JSON.stringify(value)

    );

}

function loadLocal(key) {

    const value = localStorage.getItem(key);

    return value

        ? JSON.parse(value)

        : null;

}



/* ==========================================================
   Initialize Upload Page
========================================================== */

function initializeUpload() {

    const form = document.getElementById("resumeForm");

    if (!form) return;

    form.addEventListener("submit", async function (e) {

        e.preventDefault();

        await handleResumeUpload();

    });

}

/* ==========================================================
   Handle Resume Upload
========================================================== */

async function handleResumeUpload() {

    const fileInput = document.getElementById("resume");

    const jobInput = document.getElementById("job_description");

    if (!fileInput || fileInput.files.length === 0) {

        showToast("Please select a resume file", "error");

        return;

    }

    if (!jobInput || jobInput.value.trim() === "") {

        showToast("Please enter job description", "error");

        return;

    }

    const formData = new FormData();

    formData.append("resume", fileInput.files[0]);

    formData.append("job_description", jobInput.value.trim());

    try {

        showLoader();

        const response = await fetch(API.analyze, {

            method: "POST",

            body: formData

        });

        const data = await response.json();

        hideLoader();

        if (!data.success) {

            showToast(data.message || "Analysis failed", "error");

            return;

        }

        latestResult = data;

        showToast("Resume analyzed successfully!", "success");

        console.log("Analysis Result:", data);

        // Store for other pages
        saveLocal("latestResult", data);

        // Render results if on analyze page
        if (typeof renderAnalyzeResults === "function") {

            renderAnalyzeResults(data);

        }

    }

    catch (error) {

        hideLoader();

        showToast("Server error during analysis", "error");

        console.error(error);

    }

}

/* ==========================================================
   QUICK ANALYZE BUTTON (optional support)
========================================================== */

function quickAnalyze(file, jobDescription) {

    const formData = new FormData();

    formData.append("resume", file);

    formData.append("job_description", jobDescription);

    return fetch(API.analyze, {

        method: "POST",

        body: formData

    })

    .then(res => res.json())

    .catch(err => {

        console.error(err);

        return null;

    });

}


function renderAnalyzeResults(data) {

    if (!data) return;

    /* ======================================================
       BASIC INFO
    ====================================================== */

    setText("candidateName", data.candidate_name || "--");

    /* ======================================================
       ATS SCORE
    ====================================================== */

    if (data.ats) {

        animateValue("atsScore", data.ats.ats_score || 0);

        updateProgress("atsProgress", data.ats.ats_score || 0);

        setText("atsValue", (data.ats.ats_score || 0) + "%");

        setText("atsStatus", data.ats.passed ? "PASSED" : "FAILED");

        setText("atsRating", data.ats.rating || "--");
    }

    /* ======================================================
       MATCH SCORE
    ====================================================== */

    if (data.match) {

        animateValue("matchScore", data.match.overall_score || 0);

        updateProgress("matchProgress", data.match.overall_score || 0);

        setText("matchPercentage", (data.match.overall_score || 0) + "%");

        setText("matchRecommendation", data.match.recommendation || "--");

        setText("recommendationScore", data.match.recommendation || "--");
    }

    /* ======================================================
       SKILLS
    ====================================================== */

    const skillsContainer = document.getElementById("skillsContainer");

    if (skillsContainer && data.skills) {

        skillsContainer.innerHTML = "";

        data.skills.forEach(skill => {

            skillsContainer.innerHTML += createBadge(skill, "primary");

        });

    }

    /* ======================================================
       MISSING SKILLS
    ====================================================== */

    const missingContainer = document.getElementById("missingSkillsContainer");

    if (missingContainer && data.missing_skills) {

        missingContainer.innerHTML = "";

        data.missing_skills.forEach(skill => {

            missingContainer.innerHTML += createBadge(skill, "danger");

        });

    }

    /* ======================================================
       EDUCATION
    ====================================================== */

    const eduList = document.getElementById("educationList");

    if (eduList && data.education) {

        eduList.innerHTML = "";

        data.education.forEach(item => {

            const li = document.createElement("li");

            li.textContent = item;

            eduList.appendChild(li);

        });

    }

    /* ======================================================
       EXPERIENCE
    ====================================================== */

    setText("overviewExperience", data.experience_years + " Years");

    setText("experienceDetails", data.experience_years + " Years of Experience");

    /* ======================================================
       CONFIDENCE
    ====================================================== */

    if (data.confidence) {

        animateValue("confidenceScore", data.confidence.overall_confidence || 0);

        setText("confidenceValue", data.confidence.overall_confidence + "%");
    }

    /* ======================================================
       BIAS
    ====================================================== */

    if (data.bias) {

        animateValue("biasScore", data.bias.bias_score || 0);

        updateProgress("biasProgress", data.bias.bias_score || 0);

        setText("biasStatus", data.bias.bias_risk || "No Risk Detected");

    }

    /* ======================================================
       FAKE DETECTION
    ====================================================== */

    if (data.fake) {

        animateValue("authenticityScore", data.fake.authenticity_score || 0);

        setText("verificationStatus", data.fake.verdict || "Unknown");

    }

    /* ======================================================
       INTERVIEW QUESTIONS
    ====================================================== */

    if (data.interview_questions) {

        const container = document.getElementById("aiRecommendations");

        if (container) {

            container.innerHTML = "";

            data.interview_questions.forEach(q => {

                container.innerHTML += `<li>${q}</li>`;

            });

        }

    }

    /* ======================================================
       IMPROVEMENT TIPS
    ====================================================== */

    if (data.improvement_tips) {

        const container = document.getElementById("suggestionList");

        if (container) {

            container.innerHTML = "";

            data.improvement_tips.forEach(tip => {

                container.innerHTML += `<li>${tip}</li>`;

            });

        }

    }

    /* ======================================================
       FINAL SUMMARY
    ====================================================== */

    setText(
        "finalDecision",
        data.match?.recommendation || "Analysis Completed"
    );

    setText(
        "overallSummary",
        `Candidate ${data.candidate_name} analyzed with ATS score ${data.ats?.ats_score || 0}%`
    );

    /* ======================================================
       STORE FOR OTHER PAGES
    ====================================================== */

    saveLocal("latestResult", data);

    latestResult = data;

}



/* ==========================================================
   DOWNLOAD PDF REPORT
========================================================== */

async function downloadReport() {

    if (!latestResult) {

        showToast("No report available", "error");

        return;

    }

    try {

        showLoader();

        const response = await fetch(API.downloadReport, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(latestResult)

        });

        const blob = await response.blob();

        hideLoader();

        const url = window.URL.createObjectURL(blob);

        const a = document.createElement("a");

        a.href = url;

        a.download = "AI_Resume_Report.pdf";

        document.body.appendChild(a);

        a.click();

        a.remove();

        showToast("Report downloaded successfully!", "success");

    }

    catch (error) {

        hideLoader();

        showToast("Failed to download report", "error");

        console.error(error);

    }

}

/* ==========================================================
   PRINT REPORT
========================================================== */

function printReport() {

    window.print();

}

/* ==========================================================
   COPY REPORT SUMMARY
========================================================== */

function copyReport() {

    if (!latestResult) {

        showToast("No data to copy", "error");

        return;

    }

    const text = `

Candidate: ${latestResult.candidate_name}

ATS Score: ${latestResult.ats?.ats_score || 0}%

Match Score: ${latestResult.match?.overall_score || 0}%

Recommendation: ${latestResult.match?.recommendation || "N/A"}

Skills: ${(latestResult.skills || []).join(", ")}

Missing Skills: ${(latestResult.missing_skills || []).join(", ")}

Experience: ${latestResult.experience_years || 0} years

`;

    navigator.clipboard.writeText(text);

    showToast("Report copied to clipboard!", "success");

}

/* ==========================================================
   REFRESH ANALYSIS
========================================================== */

function refreshAnalysis() {

    if (typeof handleResumeUpload === "function") {

        handleResumeUpload();

    } else {

        showToast("No active analysis", "error");

    }

}

/* ==========================================================
   VIEW HISTORY
========================================================== */

async function loadHistory() {

    const data = await apiRequest(API.history);

    if (!data) return;

    const container = document.getElementById("historyContainer");

    if (!container) return;

    container.innerHTML = "";

    data.forEach(item => {

        container.innerHTML += `

        <div class="card mt-3">

            <h3>${item.candidate_name}</h3>

            <p>ATS: ${item.ats_score}%</p>

            <p>Match: ${item.match_score}%</p>

            <p>Status: ${item.status}</p>

            <small>${formatDate(item.date)}</small>

        </div>

        `;

    });

}

/* ==========================================================
   LOAD DASHBOARD DATA
========================================================== */

async function loadDashboard() {

    const data = await apiRequest(API.dashboard);

    if (!data) return;

    dashboardData = data;

    setText("totalResumes", data.total_resumes);

    setText("averageAts", data.average_ats);

    setText("reportsGenerated", data.reports_generated);

    setText("topCandidate", data.top_candidate);

}

/* ==========================================================
   LOAD LATEST REPORT
========================================================== */

async function loadLatestReport() {

    const data = await apiRequest(API.result);

    if (!data) return;

    latestResult = data;

    setText("candidateName", data.candidate_name);

    setText("overviewCandidate", data.candidate_name);

    setText("overviewATS", data.ats?.ats_score || 0);

    setText("overviewMatch", data.match?.overall_score || 0);

    setText("overviewConfidence", data.confidence?.overall_confidence || 0);

    setText("overviewAuthenticity", data.fake?.authenticity_score || 0);

    setText("resumeSummary", "Latest resume loaded successfully.");

}



/* ==========================================================
   GLOBAL EVENT LISTENERS
========================================================== */

document.addEventListener("DOMContentLoaded", () => {

    console.log("AI Resume Screener Loaded ✔");

    bindGlobalButtons();

});

/* ==========================================================
   BIND BUTTON EVENTS
========================================================== */

function bindGlobalButtons() {

    // Upload page
    document.getElementById("uploadBtn")?.addEventListener("click", handleResumeUpload);

    // Report actions
    document.getElementById("downloadPDF")?.addEventListener("click", downloadReport);

    document.getElementById("printReport")?.addEventListener("click", printReport);

    document.getElementById("copyReport")?.addEventListener("click", copyReport);

    document.getElementById("refreshReport")?.addEventListener("click", loadLatestReport);

    // Interview page
    document.getElementById("refreshInterview")?.addEventListener("click", () => {

        showToast("Refreshing interview data...", "success");

        if (typeof initializeInterview === "function") {

            initializeInterview();

        }

    });

}

/* ==========================================================
   GLOBAL ERROR HANDLER
========================================================== */

window.addEventListener("error", (event) => {

    console.error("Global Error:", event.error);

    showToast("Something went wrong. Please try again.", "error");

});

/* ==========================================================
   NETWORK ERROR HANDLER
========================================================== */

window.addEventListener("offline", () => {

    showToast("You are offline. Check internet connection.", "error");

});

window.addEventListener("online", () => {

    showToast("Back online ✔", "success");

});

/* ==========================================================
   KEYBOARD SHORTCUTS
========================================================== */

document.addEventListener("keydown", (e) => {

    // Ctrl + U → Upload
    if (e.ctrlKey && e.key === "u") {

        e.preventDefault();

        handleResumeUpload();

    }

    // Ctrl + R → Refresh report
    if (e.ctrlKey && e.key === "r") {

        e.preventDefault();

        loadLatestReport();

    }

    // Ctrl + D → Download report
    if (e.ctrlKey && e.key === "d") {

        e.preventDefault();

        downloadReport();

    }

});

/* ==========================================================
   AUTO INITIALIZE ON PAGE LOAD
========================================================== */

(function autoInit() {

    const path = window.location.pathname;

    setTimeout(() => {

        if (path === "/dashboard") {

            loadDashboard();

        }

        if (path === "/history") {

            loadHistory();

        }

        if (path === "/report") {

            loadLatestReport();

        }

    }, 300);

})();

/* ==========================================================
   EXPORT FUNCTIONS (GLOBAL ACCESS)
========================================================== */

window.handleResumeUpload = handleResumeUpload;

window.loadDashboard = loadDashboard;

window.loadHistory = loadHistory;

window.loadLatestReport = loadLatestReport;

window.downloadReport = downloadReport;

window.printReport = printReport;

window.copyReport = copyReport;

window.refreshAnalysis = refreshAnalysis;

/* ==========================================================
   END OF SCRIPT.JS (COMPLETE)
========================================================== */

console.log("script.js fully loaded ✔");
