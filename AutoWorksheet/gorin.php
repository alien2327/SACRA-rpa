<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>Hello world!</title>
        <link href="./css/style.css" rel="stylesheet" type="text/css" />
    </head>

    <?php
    $year1 = "1964年";
    $year2 = "2020年";
    ?>

    <body>
        <div class="main-contents">
            前回の五輪は、
            <h1>
                <?php echo $year1; ?>
            </h1>
            でした。<br>
            今回の五輪は、
            <h1>
                <?php echo $year2; ?>
            </h1>
            でしたが、中止になりました。<br>
        </div>
    </body>
</html>