USE tododb;
CREATE TABLE `users` (
    `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT "ID",
    `email` VARCHAR(64) NOT NULL COMMENT "メールアドレス",
    `username` VARCHAR(64) NOT NULL COMMENT "ユーザー名",
    `password` VARCHAR(128) NOT NULL COMMENT "パスワード",
    `create_at` DATETIME NOT NULL COMMENT "ユーザー登録日時"
     );

CREATE TABLE `tasks` ( 
    `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT "taskID", 
    `title` VARCHAR(64) NOT NULL COMMENT "タイトル", 
    `detail` VARCHAR(128) NOT NULL COMMENT "本文", 
    `end_time` DATETIME NULL COMMENT "期限日時", 
    `created_at` DATETIME NOT NULL COMMENT "作成日時", 
    `update_at` DATETIME NULL COMMENT "更新日時", 
    `user_id` INT REFERENCES users(id)
);
