/* PyCore Workspace — interface behavior only.
   No API calls, business rules, or data persistence are implemented here. */
document.addEventListener("DOMContentLoaded", () => {
  const body = document.body;
  const sidebar = document.getElementById("sidebar");
  const collapseButton = document.getElementById("collapseSidebar");
  const mobileMenu = document.getElementById("mobileMenu");
  const mobileScrim = document.getElementById("mobileScrim");
  const pageLabel = document.getElementById("currentPageLabel");
  const pages = [...document.querySelectorAll(".page-section")];
  const navButtons = [...document.querySelectorAll("[data-page]")];
  const modalBackdrops = [...document.querySelectorAll(".modal-backdrop")];
  const toast = document.getElementById("prototypeToast");
  let toastTimeout;

  // Sidebar collapse/expand (visual preference only).
  collapseButton?.addEventListener("click", () => {
    body.classList.toggle("sidebar-collapsed");
    collapseButton.setAttribute(
      "aria-label",
      body.classList.contains("sidebar-collapsed") ? "Expand sidebar" : "Collapse sidebar"
    );
  });

  // Mobile navigation drawer.
  const closeMobileNav = () => body.classList.remove("mobile-nav-open");
  mobileMenu?.addEventListener("click", () => body.classList.toggle("mobile-nav-open"));
  mobileScrim?.addEventListener("click", closeMobileNav);

  // Frontend-only section switching. Django can later provide real URLs/views.
  function showPage(pageName) {
    const target = document.getElementById(`page-${pageName}`);
    if (!target) return;

    pages.forEach((page) => page.classList.toggle("active", page === target));
    navButtons.forEach((button) => {
      if (button.classList.contains("nav-item")) {
        button.classList.toggle("active", button.dataset.page === pageName);
      }
    });

    pageLabel.textContent = target.dataset.title || "Overview";
    closeMobileNav();
    window.scrollTo({ top: 0, behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });

    // Restart entrance animation when navigating between static sections.
    target.querySelectorAll(".reveal").forEach((element) => {
      element.style.animation = "none";
      void element.offsetHeight;
      element.style.animation = "";
    });
  }

  navButtons.forEach((button) => {
    button.addEventListener("click", (event) => {
      event.preventDefault();
      showPage(button.dataset.page);
    });
  });

  // Modal open/close animation. Form submission is intentionally a demo only.
  function openModal(id) {
    const modal = document.getElementById(id);
    if (!modal) return;
    modalBackdrops.forEach((item) => item.classList.remove("open"));
    modal.classList.add("open");
    body.classList.add("modal-open");
    const firstInput = modal.querySelector("input, textarea, select");
    window.setTimeout(() => firstInput?.focus(), 80);
  }

  function closeModal(modal) {
    modal.classList.remove("open");
    if (!document.querySelector(".modal-backdrop.open")) body.classList.remove("modal-open");
  }

  document.querySelectorAll("[data-open-modal]").forEach((button) => {
    button.addEventListener("click", () => openModal(button.dataset.openModal));
  });

  modalBackdrops.forEach((modal) => {
    modal.querySelectorAll(".modal-close, .modal-cancel").forEach((button) => {
      button.addEventListener("click", () => closeModal(modal));
    });
    modal.addEventListener("click", (event) => {
      if (event.target === modal) closeModal(modal);
    });
    modal.querySelector("form")?.addEventListener("submit", (event) => {
      event.preventDefault();
      closeModal(modal);
      showToast("Frontend prototype only — connect this form to Django.");
    });
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      modalBackdrops.forEach(closeModal);
      closeMobileNav();
    }
    // Search shortcut is visual convenience only.
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
      event.preventDefault();
      document.querySelector(".search-box input")?.focus();
    }
  });

  // Demo-only feedback for controls whose backend behavior is not implemented.
  function showToast(message) {
    toast.textContent = message;
    toast.classList.add("show");
    window.clearTimeout(toastTimeout);
    toastTimeout = window.setTimeout(() => toast.classList.remove("show"), 2800);
  }

  document.querySelectorAll(
    ".workspace-switcher, .text-button, .notification-button, .tiny-plus, .column-menu, .card-more, .subtle-icon, .board-project-select, .heading-actions .button:not([data-open-modal]), .filter-chip, .filter-row > .button, .activity-filter-bar > .button, .team-table-panel .icon-button"
  ).forEach((button) => {
    button.addEventListener("click", (event) => {
      if (button.dataset.page || button.dataset.openModal) return;
      if (button.classList.contains("filter-chip")) {
        const group = button.closest(".filter-chips");
        group?.querySelectorAll(".filter-chip").forEach((chip) => chip.classList.toggle("selected", chip === button));
        return;
      }
      if (button.closest(".page-section")?.id === "page-team" && button.textContent.trim() === "Manage roles") {
        showToast("Role editing will be handled by Django.");
        return;
      }
      showToast("This control is a UI prototype. Backend behavior comes later.");
    });
  });

  // Keep static prototype forms clearly separate from real backend behavior.
  document.querySelectorAll(".task-check").forEach((checkbox) => {
    checkbox.setAttribute("role", "presentation");
    checkbox.title = "Task completion will be handled by Django";
  });

  // Optional reveal observer for elements that enter the viewport.
  if ("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08 });
    document.querySelectorAll(".reveal").forEach((element) => observer.observe(element));
  }

  // Start on the Overview section.
  showPage("overview");
});