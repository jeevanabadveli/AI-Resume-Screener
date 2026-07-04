/* ==========================================================
   AI Resume Screener
   report.js
   Final Report Page Controller
========================================================== */

"use strict";

/* ==========================================================
   INIT REPORT PAGE
========================================================== */

document.addEventListener("DOMContentLoaded", () => {

    if (window.location.pathname === "/report") {

        loadReportPage();

    }

});

/* ==========================================================
   LOAD REPORT DATA
========================================================== */

async function loadReportPage() {

    try {

        const data = await apiRequest("/api/result");

        if (!data) return;

        renderReport(data);

        console.log("Report loaded ✔");

    }

    catch (error) {

        console.error("Report Error:", error);

        showToast("Failed to load report", "error");

    }

}

/* ==========================================================
   RENDER REPORT
========================================================== */

function renderReport(data) {

    latestResult = data;

    // Candidate Info
    setText("reportCandidate", data.candidate_name || "--");

    setText("reportExperience", (data.experience || 0) + " Years");

    // ATS
    setText("reportATS", data.ats?.ats_score || 0);

    // Match
    setText("reportMatch", data.match?.overall_score || 0);

    setText("reportRecommendation", data.match?.recommendation || "N/A");

    // Confidence
    setText("reportConfidence", data.confidence?.overall_confidence || 0);

    // Bias
    setText("reportBias", data.bias?.bias_score || 0);

    // Fake detection
    setText("reportAuthenticity", data.fake?.authenticity_score || 0);

    // Skills
    renderList("reportSkills", data.skills);

    // Education
    renderList("reportEducation", data.education);

    // Summary text
    setText(
        "reportSummary",
        `${data.candidate_name} has an ATS score of ${data.ats?.ats_score || 0}% and match score of ${data.match?.overall_score || 0}%.`
    );

    // Chart if available
    if (typeof initReportChart === "function") {

        initReportChart(data);

    }

}

/* ==========================================================
   RENDER LIST UTILITY
========================================================== */

function renderList(id, items) {

    const container = document.getElementById(id);

    if (!container) return;

    container.innerHTML = "";

    if (!items || items.length === 0) {

        container.innerHTML = "<li>No data</li>";

        return;

    }

    items.forEach(item => {

        const li = document.createElement("li");

        li.textContent = item;

        container.appendChild(li);

    });

}

/* ==========================================================
   DOWNLOAD REPORT PDF
========================================================== */

async function downloadReportPDF() {

    if (!latestResult) {

        showToast("No report available", "error");

        return;

    }

    try {

        const response = await fetch("/api/download-report", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify(latestResult)

        });

        const blob = await response.blob();

        const url = window.URL.createObjectURL(blob);

        const a = document.createElement("a");

        a.href = url;

        a.download = "Resume_Report.pdf";

        document.body.appendChild(a);

        a.click();

        a.remove();

        showToast("Report downloaded ✔", "success");

    }

    catch (error) {

        console.error(error);

        showToast("Download failed", "error");

    }

}

/* ==========================================================
   REFRESH REPORT
========================================================== */

async function refreshReport() {

    showToast("Refreshing report...", "success");

    await loadReportPage();

}

/* ==========================================================
   EXPORT GLOBAL FUNCTIONS
========================================================== */

window.loadReportPage = loadReportPage;

window.renderReport = renderReport;

window.downloadReportPDF = downloadReportPDF;

window.refreshReport = refreshReport;

/* ==========================================================
   END OF report.js
========================================================== */

console.log("report.js loaded ✔");