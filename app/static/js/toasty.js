/* Generated code */

function showToast({ message, type = "info", title = "Notice", delay = 5000 }) {
  const toastContainer = document.getElementById("toast-container");

  const typeClasses = {
    success: "bg-success text-white",
    error: "bg-danger text-white",
    warning: "bg-warning text-dark",
    info: "bg-info text-white",
  };

  const headerClass = typeClasses[type] || typeClasses.info;

  const toast = document.createElement("div");
  toast.className = "toast show";
  toast.setAttribute("role", "alert");
  toast.setAttribute("aria-live", "assertive");
  toast.setAttribute("aria-atomic", "true");
  toast.style.minWidth = "250px";
  toast.style.marginBottom = "1rem";

  toast.innerHTML = `
    <div class="toast-header ${headerClass}">
      <strong class="me-auto">${title}</strong>
      <small class="text-muted">Just now</small>
      <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
    <div class="toast-body">
      ${message}
    </div>
  `;

  toastContainer.appendChild(toast);

  setTimeout(() => {
    toast.classList.remove("show");
    toast.classList.add("hide");
    toast.addEventListener("transitionend", () => toast.remove());
  }, delay);
}
