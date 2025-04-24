// Navbar button functionality
document.addEventListener("DOMContentLoaded", function () {
    const navButtons = document.querySelectorAll(".nav-btn");
  
    navButtons.forEach(button => {
      button.addEventListener("click", function () {
        const page = this.textContent.trim().toLowerCase();
  
        // Handle logout separately
        if (page === "logout") {
          window.location.href = "/logout";
        } else {
          window.location.href = `/${page}`; // Navigate to route like /weekly, /monthly, etc.
        }
      });
    });
  });