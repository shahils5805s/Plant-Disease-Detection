// Drag-and-drop image upload with preview.
document.addEventListener("DOMContentLoaded", () => {
  const dropZone = document.getElementById("drop-zone");
  const fileInput = document.getElementById("file-input");
  const preview = document.getElementById("preview");
  const dropContent = dropZone ? dropZone.querySelector(".drop-zone-content") : null;
  const submitBtn = document.getElementById("submit-btn");

  if (!dropZone || !fileInput) return;

  // Highlight on drag
  ["dragenter", "dragover"].forEach(evt =>
    dropZone.addEventListener(evt, e => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.add("dragover");
    })
  );
  ["dragleave", "drop"].forEach(evt =>
    dropZone.addEventListener(evt, e => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.remove("dragover");
    })
  );

  // Handle drop
  dropZone.addEventListener("drop", e => {
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      fileInput.files = files;
      showPreview(files[0]);
    }
  });

  // Handle file picker
  fileInput.addEventListener("change", e => {
    if (e.target.files.length > 0) showPreview(e.target.files[0]);
  });

  function showPreview(file) {
    if (!file.type.match(/^image\/(png|jpe?g)$/)) {
      alert("Please choose a PNG or JPG image.");
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      alert("File too large. Maximum 5 MB.");
      return;
    }
    const reader = new FileReader();
    reader.onload = ev => {
      preview.src = ev.target.result;
      preview.hidden = false;
      if (dropContent) dropContent.style.display = "none";
      submitBtn.disabled = false;
    };
    reader.readAsDataURL(file);
  }

  // Loading state on submit
  const form = document.getElementById("upload-form");
  if (form) {
    form.addEventListener("submit", () => {
      submitBtn.textContent = "Analysing…";
      submitBtn.disabled = true;
    });
  }
});
