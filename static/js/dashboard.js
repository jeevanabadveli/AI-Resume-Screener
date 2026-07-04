/* ==========================================================
   AI Resume Screener
   dashboard.js
   Dashboard Data Handler + UI Updates
========================================================== */

"use strict";

/* ==========================================================
   LOAD DASHBOARD DATA
========================================================== */

async function loadDashboardData() {

    try {

        const response = await fetch("/api/dashboard");

        const data = await response.json();

        if (!data) return;

        updateDashboardCards(data);

        // If chart function exists (from charts.js)
        if (typeof initDashboardChart === "function") {

            initDashboardChart(data);

        }

        console.log("Dashboard loaded ✔");

    }

    catch (error) {

        console.error("Dashboard Error:", error);

    }

}

/* ==========================================================
   UPDATE DASHBOARD CARDS
========================================================== */

function updateDashboardCards(data) {

    // Total resumes
    setText("totalResumes", data.total_resumes || 0);

    animateValue("totalResumes", data.total_resumes || 0);

    // Average ATS
    setText("averageAts", (data.average_ats || 0) + "%");

    animateValue("averageAts", data.average_ats || 0);

    // Reports generated
    setText("reportsGenerated", data.reports_generated || 0);

    animateValue("reportsGenerated", data.reports_generated || 0);

    // Top candidate
    setText("topCandidate", data.top_candidate || "N/A");

}

/* ==========================================================
   LOAD ANALYTICS (Optional Extended API)
========================================================== */

async function loadAnalytics() {

    try {

        const response = await fetch("/api/analytics");

        const data = await response.json();

        if (!data) return;

        updateAnalyticsUI(data);

    }

    catch (error) {

        console.error("Analytics Error:", error);

    }

}

/* ==========================================================
   UPDATE ANALYTICS UI
========================================================== */

function updateAnalyticsUI(data) {

    setText("analyticsTotal", data.total_resumes || 0);

    setText("analyticsATS", (data.average_ats || 0) + "%");

    setText("analyticsMatch", (data.average_match || 0) + "%");

    setText("analyticsConfidence", (data.average_confidence || 0) + "%");

}

/* ==========================================================
   AUTO REFRESH DASHBOARD
========================================================== */

function startDashboardAutoRefresh() {

    setInterval(() => {

        loadDashboardData();

    }, 10000); // every 10 seconds

}

/* ==========================================================
   DASHBOARD INITIALIZER
========================================================== */

document.addEventListener("DOMContentLoaded", () => {

    if (window.location.pathname === "/dashboard") {

        loadDashboardData();

        loadAnalytics();

        startDashboardAutoRefresh();

    }

});

/* ==========================================================
   QUICK ACTIONS (Optional Buttons)
========================================================== */

function refreshDashboard() {

    loadDashboardData();

    loadAnalytics();

    showToast("Dashboard refreshed", "success");

}

/* ==========================================================
   EXPORT GLOBAL FUNCTIONS
========================================================== */

window.loadDashboardData = loadDashboardData;

window.refreshDashboard = refreshDashboard;

window.loadAnalytics = loadAnalytics;

/* ==========================================================
   END OF dashboard.js
========================================================== */

console.log("dashboard.js loaded ✔");