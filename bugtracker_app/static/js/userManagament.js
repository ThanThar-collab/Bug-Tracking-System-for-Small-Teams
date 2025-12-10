document.querySelector(".add-user-btn")?.addEventListener("click", () => {
  alert("Add new user functionality here");
});

document.querySelectorAll(".btn-edit").forEach((btn) => {
  btn.addEventListener("click", () => alert("Edit user clicked"));
});

document.querySelectorAll(".btn-delete").forEach((btn) => {
  btn.addEventListener("click", () => confirm("Delete user?"));
});
