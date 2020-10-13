<?php
$user = "root";
$password = "root";
$dbName = 'testdb';
$host = 'localhost:3307';
$dsn = "mysql:host={$host};dbname={$dbName};charset=utf8";
?>

<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>test</title>
<link href="css/style.css" rel="stylesheet">
</head>
<body>
<div>

    <?php

    try {
        $pdo = new PDO($dsn, $user, $password);
        echo "データベース {$dbName} に接続しました。";
        $sql = "SELECT * FROM test";

        $stm = $pdo->prepare($sql);

        $stm->execute();

        $result = $stm->fetchAll(PDO::FETCH_ASSOC);

        echo "<table>";
        echo "<thead><tr>";
        echo "<th>", "Name", "</th>";
        echo "<th>", "Age", "</th>";
        echo "<th>", "Sex", "</th>";
        echo "</tr></thead>";
        echo "<tbody>";
        foreach ($result as $row){
            echo "<tr>";
            echo "<td>", $row['name'], "</td>";
            echo "<td>", (string) $row['age'], "</td>";
            echo "<td>", $row['sex'], "</td>";
            echo "</tr>";
        }
        echo "</tbody>";
        echo "</table>";
    } catch (Exception $e) {
        echo '<span class="error">エラーが発生しました。</span><br>';
        echo $e->getMessage();
        exit();
    }
    ?>

</div>
</body>
</html>