<?php
$host = "localhost";
$user = "anhthi";       // đổi theo user MySQL của bạn
$pass = "anhthi060105";           // mật khẩu MySQL
$db   = "cafe_pos";

$conn = new mysqli($host, $user, $pass, $db);

// Kiểm tra kết nối
if ($conn->connect_error) {
    die("Kết nối thất bại: " . $conn->connect_error);
}

$conn->set_charset("utf8mb4");
?>
