document.querySelector(".add-bug-btn")?.addEventListener("click", () => {
  alert("Report new bug form would open here");
});

document.querySelectorAll(".btn-edit").forEach((btn) => {
  btn.addEventListener("click", () => alert("Edit bug clicked"));
});
