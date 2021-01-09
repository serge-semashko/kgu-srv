<?php
    if (!isset($_GET['callback']))
        die;
   
    include 'JSON.php';
    $callback = $_GET['callback'];
    $jsonData = file_get_contents('http://159.93.126.233:8080/proxy.cgi?id=6');
    echo JSON::enclose($callback, $cache->getData());
?>