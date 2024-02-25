<?php
$ip_server = $_SERVER['SERVER_ADDR'];

// Printing the stored address 
echo "<h1>nginx container IP Address is: $ip_server</h1>"; 

echo "<h2>Connect to database</h2>";
// Basic connection settings
$databaseHost = 'db:3306';
$databaseUsername = 'fox';
$databasePassword = 'fox123';
$databaseName = 'fox-db';

// Connect to the database
$mysqli = mysqli_connect($databaseHost, $databaseUsername, $databasePassword, $databaseName); 

if(! $mysqli ) {
    die('Could not connect: ' . mysql_error());
}

echo 'Connected successfully';
echo "<hr>";
// Fetch contacts (in descending order)
$result = mysqli_query($mysqli, "SELECT * FROM contacts");

while ($row = mysqli_fetch_assoc($result))
 {
    echo "<p><b>ID : </b>".$row['id']."<br>";
    echo "<b>Name : </b>".$row['name']."<br>";
    echo "<b>Age : </b>".$row['age']."<br>";
    echo "<b>Email : </b>".$row['email']."<br></p>";
 }

mysqli_close($mysqli);
echo 'Connection closed';

?>