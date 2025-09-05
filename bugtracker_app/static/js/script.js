const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

if (signUpButton) {
  signUpButton.addEventListener('click', () => {
    // On the login page, clicking "Register" will take you to the signup page.
    // This script is designed for the single-page version with the sliding panel.
    // We'll keep the class manipulation for now, but navigation is handled by hrefs.
    container.classList.add('right-panel-active');
  });
}

if (signInButton) {
  signInButton.addEventListener('click', () => {
    // On the signup page, clicking "Login" will take you to the login page.
    container.classList.remove('right-panel-active');
  });
}
