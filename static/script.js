// ページ読み込み時にメニューを取得して表示する
window.onload = async () => {
  try {
    // メニューAPIを呼び出し
    const menu = await fetch("/api/menu").then(res => res.json());
    const menuDiv = document.getElementById("menu-container");

    // メニューをボタンとして追加
    menu.forEach(item => {
      const btn = document.createElement("button");
      btn.textContent = item.label;
      btn.className = "btn btn-outline-primary me-2";
      // クリック時にUIを読み込む
      btn.onclick = () => loadUI(item.path);
      menuDiv.appendChild(btn);
    });
  } catch (err) {
    console.error("メニュー取得エラー:", err);
  }
};

// UI定義を取得して画面を描画する
async function loadUI(page) {
  const container = document.getElementById("content-container");
  container.innerHTML = "";

  try {
    // UI JSON を取得
    const ui = await fetch(`/api/ui/${page}`).then(res => res.json());

    if (ui.error) {
      container.innerHTML = `<div class="alert alert-danger">${ui.error}</div>`;
      return;
    }

    // タイトル表示
    container.innerHTML = `<h2>${ui.title}</h2>`;

    // 検索部品があれば描画
    if (ui.search) renderSearch(ui.search, page);

    // リスト部品があれば描画
    if (ui.list) await renderList(ui.list, page);
  } catch (err) {
    console.error("UI取得エラー:", err);
    container.innerHTML = `<div class="alert alert-danger">UI取得失敗</div>`;
  }
}

// 検索フォームを描画
function renderSearch(searchDef, page) {
  let html = `<form id="searchForm" class="mb-3">`;

  // フィルター項目を描画
  searchDef.filters.forEach(f => {
    html += `<input name="${f.field}" placeholder="${f.placeholder}" class="form-control mb-2">`;
  });

  // アクションボタンを描画
  searchDef.actions.forEach(btn => {
    html += `<button type="${btn.type}" class="${btn.class} me-2">${btn.label}</button>`;
  });

  html += `</form>`;
  document.getElementById("content-container").innerHTML += html;

  // フォーム送信時の処理
  document.getElementById("searchForm").addEventListener("submit", async e => {
    e.preventDefault();
    await renderList({ source: `/api/${page}` }, page); // URL の先頭に / を追加
  });

  // フォームリセット時の処理
  document.getElementById("searchForm").addEventListener("reset", async e => {
    e.preventDefault();
    document.getElementById("searchForm").reset();
    await renderList({ source: `/api/${page}` }, page); // URL の先頭に / を追加
  });
}

// リストを描画
async function renderList(listDef, page) {
  try {
    // 検索フォームからクエリ文字列を作成
    const form = document.getElementById("searchForm");
    let query = "";
    if (form) {
      const formData = new FormData(form);
      const params = new URLSearchParams(formData);
      query = "?" + params.toString();
    }

    // fetch でデータ取得
    const res = await fetch(`${listDef.source}${query}`); // listDef.source に先頭 / が含まれている想定
    if (!res.ok) throw new Error(`HTTPエラー ${res.status}`);

    const data = await res.json();
    const container = document.getElementById("content-container");

    // テーブルヘッダー
    let html = `<table class="table table-striped"><thead><tr>`;
    listDef.columns.filter(c => c.visible).forEach(c => {
      html += `<th>${c.label}</th>`;
    });
    html += `</tr></thead><tbody>`;

    // テーブルボディ
    data.forEach(row => {
      html += `<tr>`;
      listDef.columns.filter(c => c.visible).forEach(c => {
        let value = row[c.field];
        html += `<td>${value ?? ""}</td>`;
      });
      html += `</tr>`;
    });

    html += `</tbody></table>`;
    container.innerHTML += html;
  } catch (err) {
    console.error("リスト描画エラー:", err);
  }
}
