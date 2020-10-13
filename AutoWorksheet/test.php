<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>TEST</title>
<link href="css/style.css" rel="stylesheet">
</head>
<body>
<div>

<?php

require 'PhpSpreadsheet/vendor/autoload.php';
require 'japanese-holiday/vendor/autoload.php';

use PhpOffice\PhpSpreadsheet\Spreadsheet;
use PhpOffice\PhpSpreadsheet\Reader\Xlsx as XlsxReader;
use PhpOffice\PhpSpreadsheet\Writer\Xlsx as XlsxWriter;
use Japanese\Holiday\Repository as HolidayRepository;

fromSql();

function createSheet($year, $month) {
    $date = $year.'-'.$month;
    $lastDate = (int) date('d', strtotime('last day of ' . $date));
    $holidayRepository = new HolidayRepository();
    $early = 16;
    $late = 15;
    $c_1 = ['B','C','D','E','F','G','H','I','J','K','L','M','N'];
    $c_2 = ['P','Q','R','S','T','U','V','W','X','Y','Z','AA','AB'];
    $col = [$c_1, $c_2];
    $r_1 = [];
    $r_2 = [];
    for ($i=0; $i<16; $i++){
        $r_1[] = (string) 5+2*$i;
    }
    for ($i=0; $i<15; $i++){
        $r_2[] = (string) 5+2*$i;
    }
    $row = [$r_1, $r_2];
    $spreadsheet = new Spreadsheet();
    $sheet = $spreadsheet->getActiveSheet();
    
    for ($i=0; $i<36; $i++){
        $sheet->getRowDimension((string)$i)->setRowHeight(18.75);
    }

    $styleArray = [
        'borders' => [
            'allBorders' => [
                'borderStyle' => \PhpOffice\PhpSpreadsheet\Style\Border::BORDER_THIN,
                'color' => ['argb' => 'FF000000'],
            ],
        ],
        'alignment' => [
            'horizontal' => PhpOffice\PhpSpreadsheet\Style\Alignment::HORIZONTAL_CENTER,
            'vertical' => PhpOffice\PhpSpreadsheet\Style\Alignment::VERTICAL_CENTER,
            'wrapText' => true,
        ],
    ];

    $sheet->getStyle('B2:N36')->applyFromArray($styleArray);
    $sheet->getStyle('P2:AB36')->applyFromArray($styleArray);

    $styleArray = [  
        'borders' => [  
            'diagonal' => [  
                'borderStyle' => \PhpOffice\PhpSpreadsheet\Style\Border::BORDER_THIN,  
                'color' => ['argb' => 'FF000000'],  
            ],  
            'diagonalDirection' => \PhpOffice\PhpSpreadsheet\Style\Borders::DIAGONAL_DOWN,  
        ],  
    ];

    for ($tag=0; $tag<2; $tag++){
        $sheet->setCellValue($col[$tag][0].'2', '日付');
        $sheet->mergeCells($col[$tag][0].'2:'.$col[$tag][0].'4');
        $sheet->setCellValue($col[$tag][1].'2', '作業者印(始業)');
        $sheet->mergeCells($col[$tag][1].'2:'.$col[$tag][1].'4');
        $sheet->setCellValue($col[$tag][2].'2', '勤務内容');
        $sheet->mergeCells($col[$tag][2].'2:'.$col[$tag][10].'2');
        $sheet->setCellValue($col[$tag][2].'3', '業務内容');
        $sheet->mergeCells($col[$tag][2].'3:'.$col[$tag][2].'4');
        $sheet->setCellValue($col[$tag][3].'3', '定められた勤務時間');
        $sheet->mergeCells($col[$tag][3].'3:'.$col[$tag][3].'4');
        $sheet->getStyle($col[$tag][3].'3:'.$col[$tag][3].'4')->getFont()->setSize(8);
        $sheet->setCellValue($col[$tag][4].'3', '減額時間');
        $sheet->mergeCells($col[$tag][4].'3:'.$col[$tag][4].'4');
        $sheet->setCellValue($col[$tag][5].'3', '(休憩時間)');
        $sheet->mergeCells($col[$tag][5].'3:'.$col[$tag][6].'3');
        $sheet->setCellValue($col[$tag][5].'4', '超過勤務時間');
        $sheet->mergeCells($col[$tag][5].'4:'.$col[$tag][6].'4');
        $sheet->setCellValue($col[$tag][7].'3', '超過勤務等');
        $sheet->setCellValue($col[$tag][7].'4', '100/100');
        $sheet->setCellValue($col[$tag][8].'4', '125/100');
        $sheet->setCellValue($col[$tag][9].'4', '25/100');
        $sheet->mergeCells($col[$tag][7].'3:'.$col[$tag][9].'3');
        $sheet->setCellValue($col[$tag][10].'3', 'その他');
        $sheet->mergeCells($col[$tag][10].'3:'.$col[$tag][10].'4');
        $sheet->setCellValue($col[$tag][11].'2', '監督・命令者認印');
        $sheet->mergeCells($col[$tag][11].'2:'.$col[$tag][11].'4');
        $sheet->setCellValue($col[$tag][12].'2', '従事者印(超勤)');
        $sheet->mergeCells($col[$tag][12].'2:'.$col[$tag][12].'4');
    
        foreach ($row[$tag] as $j => $r) {
            $d = $j + 1 + $early*$tag;
            if ($d>$lastDate) {
                foreach ($col[$tag] as $c) {
                    $ran = $c.(string)$r.':'.$c.(string)($r+1);
                    $sheet->mergeCells($ran);
                    $sheet->getStyle($ran)->applyFromArray($styleArray);
                }
            } else {
                foreach ($col[$tag] as $i=>$c) {
                    if (($i==5) || ($i==6)) {
                        $sheet->setCellValue($c.(string)$r, '(　：　)');
                        $sheet->setCellValue($c.(string)($r+1), ':');
                    } else {
                        if ($i==0) {
                            $sheet->setCellValue($c.(string)$r, (string)$d);
                        }
                        if ($i==2) {
                            $holiday = $holidayRepository->isHoliday($year.'-'.$month.'-'.(string)$d);
                            $weekend = new DateTime($year.'-'.$month.'-'.(string)$d);
                            $w = (int)date_format($weekend, 'w');
                            if ($holiday==1) {
                                $sheet->setCellValue($c.(string)$r, '(祝日)');
                            } else if ($w==6) {
                                $sheet->setCellValue($c.(string)$r, '(土曜)');
                            } else if ($w==0) {
                                $sheet->setCellValue($c.(string)$r, '(日曜)');
                            }
                        }
                        $ran = $c.(string)$r.':'.$c.(string)($r+1);
                        $sheet->mergeCells($ran);
                    }
                }
            }
    
        }
    }
    
    foreach ($col[1] as $i=>$c){
        if ($i==0) {
            $sheet->setCellValue($c.'35', "計");
            $sheet->mergeCells($c."35:".$col[1][$i+2]."36");
        } else if (($i==3) || ($i==4) || ($i==7) || ($i==8) || ($i==9) || ($i==10)) {
            $sum = '=SUM('.$col[0][$i].'5:'.$col[0][$i].'36,'.$col[1][$i].'5:'.$col[1][$i].'34)';
            $sheet->setCellValue($col[1][$i].'35', $sum);
            $sheet->mergeCells($c.'35:'.$c.'36');
        } else if (($i==5) || ($i==11)) {
            $sheet->mergeCells($c.'35:'.$col[1][$i+1].'36');
            $sheet->getStyle($c.'35:'.$col[1][$i+1].'36')->applyFromArray($styleArray);
        }
    }
    
    $writer = new XlsxWriter($spreadsheet);
    $writer->save('temp'.'_'.$year.$month.'.xlsx');
}

function readSheet($year, $month) {
    $date = $year.'-'.$month;
    $lastDate = (int) date('d', strtotime('last day of ' . $date));
    $early = 16;
    $late = 15;
    $c_1 = ['B','C','D','E','F','G','H','I','J','K','L','M','N'];
    $c_2 = ['P','Q','R','S','T','U','V','W','X','Y','Z','AA','AB'];
    $col = [$c_1, $c_2];
    $r_1 = [];
    $r_2 = [];
    for ($i=0; $i<16; $i++){
        $r_1[] = (string) 5+2*$i;
    }
    for ($i=0; $i<15; $i++){
        $r_2[] = (string) 5+2*$i;
    }
    $row = [$r_1, $r_2];
    $path = './temp_'.$year.$month.'.xlsx';
    $reader = new XlsxReader();
    $spreadSheet = $reader->load($path);
    $sheet = $spreadSheet->getActiveSheet();

    $data = [];

    for ($tag=0; $tag<2; $tag++) {
        foreach ($row[$tag] as $i=>$r) {
            $value = [$month];
            foreach ($col[$tag] as $j=>$c) {
                if (($j==1) || ($j==11) || ($j==12)) {
                    continue;
                } else if (($j==3) || ($j==4) || ($j==7) || ($j==8) || ($j==9) || ($j==10)) {
                    $value[] = (float) $sheet->getCell($c.(string)$r)->getValue();
                } else if (($j==5) || ($j==6)) {
                    $value[] = $sheet->getCell($c.(string)$r)->getValue();
                    $value[] = $sheet->getCell($c.(string)($r+1))->getValue();
                } else {
                    $value[] = $sheet->getCell($c.(string)$r)->getValue();
                }
            }
            if ($i+$early*$tag+1 == $lastDate) {
                $data[] = $value;
                $value = $sheet->rangeToArray('P35:AB35');
                $data = array_merge($data, $value);
                break; 
            }
            $data[] = $value;
        }
    }

    return $data;
}

function toSql($data) {
    $user = "root";
    $password = "root";
    $dbName = 'testdb';
    $host = 'localhost:3307';
    $dsn = "mysql:host={$host};dbname={$dbName};charset=utf8";
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
        print_r($sql);
        $stm = $pdo->prepare($sql);
        $check = $stm->execute();
        if ($check) {
            print_r("Done");
        } else {
            print_r("Fail");
        }
    } catch (Exception $e) {
        echo '<span class="error">エラーが発生しました。</span><br>';
        echo $e->getMessage();
        exit();
    }
}

function fromSql() {
    $user = "root";
    $password = "root";
    $dbName = 'testdb';
    $host = 'localhost:3307';
    $dsn = "mysql:host={$host};dbname={$dbName};charset=utf8";
    try {
        $pdo = new PDO($dsn, $user, $password);
        echo "データベース {$dbName} に接続しました。";
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
    } catch (Exception $e) {
        echo '<span class="error">エラーが発生しました。</span><br>';
        echo $e->getMessage();
        exit();
    }
}

?>

</div>
</body>
</html>