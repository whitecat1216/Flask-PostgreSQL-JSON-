-- メニュー
CREATE TABLE menus (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  path VARCHAR(100)
);

INSERT INTO menus (name, path) VALUES
('社員一覧', '/employees'),
('部署一覧', '/departments');

-- 社員
CREATE TABLE employees (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  department VARCHAR(100)
);

INSERT INTO employees (name, department) VALUES
('田中 太郎', '営業'),
('佐藤 花子', '開発'),
('鈴木 次郎', '総務');
