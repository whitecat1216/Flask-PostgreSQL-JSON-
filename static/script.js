window.onload = () => {
  loadMenus();
  loadEmployees();
};

// 🔹 メニュー一覧を読み込み
function loadMenus() {
  fetch("/api/menus")
    .then(res => res.json())
    .then(data => {
      const ul = document.getElementById("menuList");
      ul.innerHTML = "";
      data.forEach(menu => {
        const li = document.createElement("li");
        li.classList.add("list-group-item", "d-flex", "justify-content-between", "align-items-center");
        li.innerHTML = `
          <span>${menu.name}</span>
          <span class="badge bg-primary">${menu.path}</span>
        `;
        ul.appendChild(li);
      });
    })
    .catch(err => console.error("メニュー取得エラー:", err));
}

// 🔹 社員一覧を読み込み
function loadEmployees() {
  fetch("/api/employees")
    .then(res => res.json())
    .then(data => {
      const tbody = document.querySelector("#empTable tbody");
      tbody.innerHTML = "";
      data.forEach(emp => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${emp.id}</td>
          <td>${emp.name}</td>
          <td>${emp.department}</td>
        `;
        tbody.appendChild(tr);
      });
    })
    .catch(err => console.error("社員取得エラー:", err));
}
