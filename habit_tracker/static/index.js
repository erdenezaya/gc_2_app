// JS for index.html page
// open the login form when user clicks on the login button
function openLoginForm() {
  const modal = document.getElementById("loginForm");
  modal.style.display = "flex";
  const form = modal.querySelector('.form-content');
  form.style.animation = "none";           // remove animation
  form.offsetHeight;                       // trigger reflow
  form.style.animation = "popupScale 0.3s ease-out forwards";  // reapply animation       
}

// close the login form
function closeLoginForm() { 
  const modal = document.getElementById("loginForm");
  modal.style.display = "none";
}

// open the signup form when user clicks on the signup button
function openSignupForm() {
  const modal = document.getElementById("signupForm");
  modal.style.display = "flex";
  const form = modal.querySelector('.form-content');
  form.style.animation = "none";           // remove animation
  form.offsetHeight;                       // trigger reflow
  form.style.animation = "popupScale 0.3s ease-out forwards";  // reapply animation
}
// close the signup form
function closeSignupForm() { 
  const modal = document.getElementById("signupForm");
  modal.style.display = "none";
}