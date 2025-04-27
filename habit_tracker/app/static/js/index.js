// ------------------ Login form pop up ---------
function openLoginForm() {
  const modal = document.getElementById("loginForm");
  modal.style.display = "flex";
  const form = modal.querySelector('.form-content');
  form.style.animation = "none";           // remove animation
  form.offsetHeight;                       // trigger reflow
  form.style.animation = "popupScale 0.3s ease-out forwards";  // reapply animation       
}

function closeLoginForm() { 
  const modal = document.getElementById("loginForm");
  modal.style.display = "none";
}

// ------------------ Signup form pop up ---------
function openSignupForm() {
  const modal = document.getElementById("signupForm");
  modal.style.display = "flex";
  const form = modal.querySelector('.form-content');
  form.style.animation = "none";           // remove animation
  form.offsetHeight;                       // trigger reflow
  form.style.animation = "popupScale 0.3s ease-out forwards";  // reapply animation
}

function closeSignupForm() { 
  const modal = document.getElementById("signupForm");
  modal.style.display = "none";
}