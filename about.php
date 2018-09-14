<?php
$servername = "mydbinstance.clbweyw8lzno.us-east-2.rds.amazonaws.com";
$username = "root";
$password = "1127544165Aa";

// Create connection
$conn = new mysqli($servername, $username, $password);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 
echo "Connected successfully";
?>