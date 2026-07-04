/* ==========================================================
   AI Resume Screener
   upload.js
   Handles Resume Upload + Analysis Trigger
========================================================== */

"use strict";

/* ==========================================================
   INIT UPLOAD PAGE
========================================================== */

document.addEventListener("DOMContentLoaded", () => {

    if (window.location.pathname === "/analyze") {

        initializeUploadForm();

    }

});

/* ==========================================================
   INITIALIZE FORM
========================================================== */

function initializeUploadForm() {

    const form = document.getElementById("resumeForm");

    if (!form) return;

    form.addEventListener("submit", (e) => {

        e.preventDefault();

        uploadResume();

    });

}

/* ==========================================================
   MAIN UPLOAD FUNCTION
========================================================== */

async function uploadResume() {

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

    const file = fileInput.files[0];

    /* ======================================================
       VALIDATION
    ====================================================== */

    if (!file.name.endsWith(".pdf")) {

        showToast("Only PDF files are allowed", "error");

        return;

    }

    const formData = new FormData();

    formData.append("resume", file);

    formData.append("job_description", jobInput.value.trim());

    try {

        showUploadProgress();

        const response = await fetch("/api/analyze", {

            method: "POST",

            body: formData

        });

        const data = await response.json();

        hideUploadProgress();

        if (!data.success) {

            showToast(data.message || "Upload failed", "error");

            return;

        }

        showToast("Resume analyzed successfully ✔", "success");

        // Store globally for other pages
        latestResult = data;

        saveLocal("latestResult", data);

        // Render results if function exists
        if (typeof renderAnalyzeResults === "function") {

            renderAnalyzeResults(data);

        }

        console.log("Upload complete ✔", data);

    }

    catch (error) {

        hideUploadProgress();

        console.error(error);

        showToast("Server error during upload", "error");

    }

}

/* ==========================================================
   UPLOAD PROGRESS UI
========================================================== */

function showUploadProgress() {

    const progress = document.getElementById("uploadProgress");

    if (progress) {

        progress.style.display = "block";

        progress.style.width = "0%";

        let width = 0;

        const interval = setInterval(() => {

            if (width >= 90) {

                clearInterval(interval);

            }

            width += 10;

            progress.style.width = width + "%";

        }, 200);

    }

}

function hideUploadProgress() {

    const progress = document.getElementById("uploadProgress");

    if (progress) {

        progress.style.width = "100%";

        setTimeout(() => {

            progress.style.display = "none";

        }, 300);

    }

}

/* ==========================================================
   FILE PREVIEW
========================================================== */

function previewFile(input) {

    const file = input.files[0];

    const preview = document.getElementById("filePreview");

    if (!file || !preview) return;

    preview.innerHTML = `
        <div class="file-info">
            <p><strong>${file.name}</strong></p>
            <p>${(file.size / 1024).toFixed(2)} KB</p>
        </div>
    `;
}

/* ==========================================================
   RESET UPLOAD FORM
========================================================== */

function resetUpload() {

    document.getElementById("resumeForm")?.reset();

    const preview = document.getElementById("filePreview");

    if (preview) {

        preview.innerHTML = "";

    }

    showToast("Form reset ✔", "success");

}

/* ==========================================================
   GLOBAL EXPORT
========================================================== */

window.uploadResume = uploadResume;
window.previewFile = previewFile;
window.resetUpload = resetUpload;

/* ==========================================================
   END OF upload.js
========================================================== */

console.log("upload.js loaded ✔");