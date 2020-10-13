<?php
$columns = ['month','day','content','work time','reduction time','rest time(1)','overwork time(1)','rest time(2)','overwork time(2)','overwork(100/100)','overwork(125/100)','overwork(25/100)','other'];
$text = "start";
foreach ($columns as $t) {
    $text .= ",".$t;
}
echo count($columns);
?>