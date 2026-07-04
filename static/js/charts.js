/* ==========================================================
   AI Resume Screener
   charts.js
   All Dashboard + Report Charts
========================================================== */

"use strict";

/* ==========================================================
   GLOBAL CHART STORAGE
========================================================== */

let dashboardChart = null;
let reportChart = null;
let historyChart = null;

/* ==========================================================
   INIT DASHBOARD CHART
========================================================== */

function initDashboardChart(data) {

    const ctx = document.getElementById("dashboardChart");

    if (!ctx || !data) return;

    if (dashboardChart) {

        dashboardChart.destroy();

    }

    dashboardChart = new Chart(ctx, {

        type: "bar",

        data: {

            labels: ["ATS", "Match", "Confidence"],

            datasets: [{

                label: "Score (%)",

                data: [

                    data.average_ats || 0,

                    data.average_match || 0,

                    data.average_confidence || 0

                ],

                backgroundColor: [

                    "#4CAF50",

                    "#2196F3",

                    "#FF9800"

                ],

                borderRadius: 10

            }]

        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    display: false

                }

            },

            scales: {

                y: {

                    beginAtZero: true,

                    max: 100

                }

            }

        }

    });

}

/* ==========================================================
   REPORT CHART (ATS + MATCH + CONFIDENCE)
========================================================== */

function initReportChart(data) {

    const ctx = document.getElementById("reportChart");

    if (!ctx || !data) return;

    if (reportChart) {

        reportChart.destroy();

    }

    reportChart = new Chart(ctx, {

        type: "doughnut",

        data: {

            labels: ["ATS Score", "Match Score", "Confidence"],

            datasets: [{

                data: [

                    data.ats?.ats_score || 0,

                    data.match?.overall_score || 0,

                    data.confidence?.overall_confidence || 0

                ],

                backgroundColor: [

                    "#00C853",

                    "#2962FF",

                    "#FF6D00"

                ],

                borderWidth: 2

            }]

        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    position: "bottom"

                }

            }

        }

    });

}

/* ==========================================================
   HISTORY CHART (TREND ANALYSIS)
========================================================== */

function initHistoryChart(historyData) {

    const ctx = document.getElementById("historyChart");

    if (!ctx || !historyData) return;

    if (historyChart) {

        historyChart.destroy();

    }

    const labels = historyData.map(item => item.candidate_name);

    const atsScores = historyData.map(item => item.ats_score);

    const matchScores = historyData.map(item => item.match_score);

    historyChart = new Chart(ctx, {

        type: "line",

        data: {

            labels: labels,

            datasets: [

                {

                    label: "ATS Score",

                    data: atsScores,

                    borderColor: "#4CAF50",

                    fill: false,

                    tension: 0.3

                },

                {

                    label: "Match Score",

                    data: matchScores,

                    borderColor: "#2196F3",

                    fill: false,

                    tension: 0.3

                }

            ]

        },

        options: {

            responsive: true,

            scales: {

                y: {

                    beginAtZero: true,

                    max: 100

                }

            }

        }

    });

}

/* ==========================================================
   INTERVIEW ANALYTICS CHART
========================================================== */

function initInterviewChart(data) {

    const ctx = document.getElementById("questionChart");

    if (!ctx || !data) return;

    new Chart(ctx, {

        type: "pie",

        data: {

            labels: ["Easy", "Medium", "Hard"],

            datasets: [{

                data: [

                    data.easy || 0,

                    data.medium || 0,

                    data.hard || 0

                ],

                backgroundColor: [

                    "#4CAF50",

                    "#FF9800",

                    "#F44336"

                ]

            }]

        },

        options: {

            responsive: true

        }

    });

}

/* ==========================================================
   AUTO INITIALIZE CHARTS
========================================================== */

document.addEventListener("DOMContentLoaded", async () => {

    try {

        // Dashboard page
        if (window.location.pathname === "/dashboard") {

            const res = await fetch("/api/dashboard");

            const data = await res.json();

            initDashboardChart(data);

        }

        // Report page
        if (window.location.pathname === "/report") {

            const res = await fetch("/api/result");

            const data = await res.json();

            initReportChart(data);

        }

        // History page
        if (window.location.pathname === "/history") {

            const res = await fetch("/api/history");

            const data = await res.json();

            initHistoryChart(data);

        }

    }

    catch (err) {

        console.error("Chart init error:", err);

    }

});

/* ==========================================================
   EXPORT FUNCTIONS
========================================================== */

window.initDashboardChart = initDashboardChart;
window.initReportChart = initReportChart;
window.initHistoryChart = initHistoryChart;

/* ==========================================================
   END OF charts.js
========================================================== */

console.log("charts.js loaded ✔");