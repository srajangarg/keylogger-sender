<?php
	$con = $_GET["q"];
	$name = $_GET["n"];

	$time1 = date('H-i-s d-m-Y');
	$time1 = $time1 . '.txt';

	if (!file_exists($name)) 
	{
	    mkdir($name, 0777, true);
	}

	$handle = fopen($name.'/'.$time1,'w');
	fwrite($handle, $con);
	fclose($handle);
?>