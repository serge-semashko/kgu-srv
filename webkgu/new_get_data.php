<?php
    function writeLog($text)
    {
        $file = fopen("log.txt", "a+");
        $today = date("d.m.y H:i:s");
        fwrite($file, $today . " > " . $text);
    }

    if (!isset($_GET['callback']))
        die;
	$jsonData = file_get_contents('http://10.0.10.103:9090/get_data=1&callback=?');
	writeLog("B" . strlen($jsonData) ." ". $jsonData);
	$jsonData = substr($jsonData,1,strlen($jsonData)-5);
	writeLog("A" . strlen($jsonData) ." ". $jsonData);
	echo $jsonData;
?>