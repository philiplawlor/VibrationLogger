<?php
class MyDB extends SQLite3 {
      function __construct() {
         $this->open('/home/pi/Documents/logs.db');
      }
}

   $db = new MyDB();
   if(!$db) {
      $msg = $db->lastErrorMsg();
   } else {
      //echo "Opened database successfully\n";
      $msg = "Water Running Detector\n";
   }

   $sql =<<<EOF
      SELECT row_number() over(order by date) id, * from log order by 1 desc LIMIT 40;
   EOF;

   $ret = $db->query($sql);

?>

<HTML>
<Title>Water Running Detector</Title>
<meta http-equiv="refresh" content="300"/>
<style>
	body {color:yellow;}
	table {color:yellow;}
</style>

<BODY color=white bgcolor=black>
</BR></BR>
<?= $msg ?>
<table >
<tr><th colspan=3><?= date('Y-m-d H:i:s'); ?></th></tr>
<?php 
   while($row = $ret->fetchArray(SQLITE3_ASSOC)) {
//var_dump($row);   
	echo "<TR>";   
	   echo "<td>" . $row['id'] . "</td>";
	   echo "<td>" . $row['date'] . "</td>";
	   echo "<td>" . $row['text'] . "</td>";
	   echo "<td>" . $row['calledBy'] . "</td>";
   	echo "</TR>";
   }

?>
</table>
</BODY>
</HTML>


