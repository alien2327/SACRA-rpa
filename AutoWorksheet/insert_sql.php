<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>Recording</title>
<link href="css/style.css" rel="stylesheet">
</head>
<body>
<div>

<?php
$user = "root";
$password = "root";
$dbName = 'testdb';
$host = 'localhost:3307';
$dsn = "mysql:host={$host};dbname={$dbName};charset=utf8";

$name = $_POST["name"];
$month = $_POST["month"];
$day = $_POST["day"];
$content = $_POST["content"];
$worktime = $_POST["worktime"];
$reduced = $_POST["reduced"];
$rest_1 = $_POST["rest_1"];
$over_1 = $_POST["over_1"];
$rest_2 = $_POST["rest_2"];
$over_2 = $_POST["over_2"];
$over_100 = $_POST["over_100"];
$over_125 = $_POST["over_125"];
$over_25 = $_POST["over_25"];
$other = $_POST["other"];

$data = [];
$buf = [(string) $month, (string) $day, $content, $worktime, $reduced, (string) $rest_1, (string) $over_1, (string) $rest_2, (string) $over_2, $over_100, $over_125, $over_25, $other];

for ($i=0; $i<30; $i++) {
    $data[$i] = $buf;
}

try {

    $pdo = new PDO($dsn, $user, $password);
    echo "データベース {$dbName} に接続しました。\n";
    $sql = "INSERT INTO rpa_test (月,日,業務内容,勤務時間,減額時間,休憩時間_1,超過勤務時間_1,休憩時間_2,超過勤務時間_2,超過勤務等_100,超過勤務等_125,超過勤務等_25,その他) VALUES ";
    $col = "";
    foreach ($data as $j=>$row) {
        if ($j < count($data)-2){
            $col = "(";
            foreach ($row as $i=>$t) {
                if (is_string($t)) {
                    if ($i!=12) {
                        $col .= "'".$t."', ";
                    } else {
                        $col .= "'".$t."'";
                    } 
                } else if (is_int($t) || (is_float($t))) {
                    if ($i!=12) {
                        $col .= $t.", ";
                    } else {
                        $col .= $t;
                    } 
                }
            }
            $col .= "), ";
            $sql .= $col;
        } else if ($j == count($data)-2) {
            $col = "(";
            foreach ($row as $i=>$t) {
                if (is_string($t)) {
                    if ($i!=12) {
                        $col .= "'".$t."', ";
                    } else {
                        $col .= "'".$t."'";
                    } 
                } else if (is_int($t) || (is_float($t))) {
                    if ($i!=12) {
                        $col .= $t.", ";
                    } else {
                        $col .= $t;
                    } 
                }
            }
            $col .= ")";
            $sql .= $col;
        }
    }
    $stm = $pdo->prepare($sql);
    $check = $stm->execute();
    if ($check) {
        $sql = "SELECT * FROM rpa_test";
        $stm = $pdo->prepare($sql);
        $stm->execute();
        $result = $stm->fetchAll(PDO::FETCH_ASSOC);
        echo "<table>";
        echo "<thead><tr>";
        echo "<th>", "月", "</th>";
        echo "<th>", "日", "</th>";
        echo "<th>", "業務内容", "</th>";
        echo "<th>", "勤務時間", "</th>";
        echo "<th>", "減額時間", "</th>";
        echo "<th>", "休憩時間_1", "</th>";
        echo "<th>", "超過勤務時間_1", "</th>";
        echo "<th>", "休憩時間_2", "</th>";
        echo "<th>", "超過勤務時間_2", "</th>";
        echo "<th>", "超過勤務等_100", "</th>";
        echo "<th>", "超過勤務等_125", "</th>";
        echo "<th>", "超過勤務等_25", "</th>";
        echo "<th>", "その他", "</th>";
        echo "</tr></thead>";
        echo "<tbody>";
        foreach ($result as $row){
            echo "<tr>";
            echo "<td>", (string) $row['月'], "</td>";
            echo "<td>", (string) $row['日'], "</td>";
            echo "<td>", (string) $row['業務内容'], "</td>";
            echo "<td>", (string) $row['勤務時間'], "</td>";
            echo "<td>", (string) $row['減額時間'], "</td>";
            echo "<td>", (string) $row['休憩時間_1'], "</td>";
            echo "<td>", (string) $row['超過勤務時間_1'], "</td>";
            echo "<td>", (string) $row['休憩時間_2'], "</td>";
            echo "<td>", (string) $row['超過勤務時間_2'], "</td>";
            echo "<td>", (string) $row['超過勤務等_100'], "</td>";
            echo "<td>", (string) $row['超過勤務等_125'], "</td>";
            echo "<td>", (string) $row['超過勤務等_25'], "</td>";
            echo "<td>", (string) $row['その他'], "</td>";
            echo "</tr>";
        }
        echo "</tbody>";
        echo "</table>";
    } else {
        print_r("Fail");
    }
} catch (Exception $e) {
    echo '<span class="error">エラーが発生しました。</span><br>';
    echo $e->getMessage();
    exit();
}
?>

<hr>
<p><a href="<?php echo $gobackURL ?>">戻る</a></p>

</div>
</body>
</head>
</html>