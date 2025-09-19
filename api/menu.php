<?php
// CORS headers
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");
header("Content-Type: application/json; charset=UTF-8");

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

require_once "db.php";

$method = $_SERVER['REQUEST_METHOD'];

try {
    switch ($method) {
        case 'GET':
            // Lấy danh sách theo category
            $category = $_GET['category'] ?? '';
            if ($category) {
                $stmt = $conn->prepare("SELECT id, name, price, category FROM menu_items WHERE category=? ORDER BY id ASC");
                $stmt->bind_param("s", $category);
                $stmt->execute();
                $result = $stmt->get_result();
            } else {
                $result = $conn->query("SELECT id, name, price, category FROM menu_items ORDER BY id ASC");
            }
            $data = [];
            while ($row = $result->fetch_assoc()) {
                $data[] = $row;
            }
            echo json_encode($data);
            break;

        case 'POST':
            // Thêm món mới
            $input = json_decode(file_get_contents("php://input"), true);
            if (!$input || !isset($input['name'], $input['price'], $input['category'])) {
                http_response_code(400);
                echo json_encode(["error" => "Missing required fields"]);
                break;
            }
            $stmt = $conn->prepare("INSERT INTO menu_items (name, price, category) VALUES (?, ?, ?)");
            $stmt->bind_param("sis", $input['name'], $input['price'], $input['category']);
            $stmt->execute();
            $newId = $conn->insert_id;
            echo json_encode([
                "id" => $newId,
                "name" => $input['name'],
                "price" => $input['price'],
                "category" => $input['category']
            ]);
            break;

        case 'PUT':
            // Cập nhật món
            parse_str($_SERVER['QUERY_STRING'], $query);
            $id = intval($query['id'] ?? 0);
            if (!$id) {
                http_response_code(400);
                echo json_encode(["error" => "Missing ID"]);
                break;
            }
            $input = json_decode(file_get_contents("php://input"), true);
            if (!$input) {
                http_response_code(400);
                echo json_encode(["error" => "Invalid JSON"]);
                break;
            }
            $stmt = $conn->prepare("UPDATE menu_items SET name=?, price=?, category=? WHERE id=?");
            $stmt->bind_param("sisi", $input['name'], $input['price'], $input['category'], $id);
            $stmt->execute();
            if ($stmt->affected_rows === 0) {
                http_response_code(404);
                echo json_encode(["error" => "Item not found"]);
            } else {
                echo json_encode([
                    "id" => $id,
                    "name" => $input['name'],
                    "price" => $input['price'],
                    "category" => $input['category']
                ]);
            }
            break;

        case 'DELETE':
            // Xóa món
            parse_str($_SERVER['QUERY_STRING'], $query);
            $id = intval($query['id'] ?? 0);
            if (!$id) {
                http_response_code(400);
                echo json_encode(["error" => "Missing ID"]);
                break;
            }
            $stmt = $conn->prepare("DELETE FROM menu_items WHERE id=?");
            $stmt->bind_param("i", $id);
            $stmt->execute();
            if ($stmt->affected_rows === 0) {
                http_response_code(404);
                echo json_encode(["error" => "Item not found"]);
            } else {
                http_response_code(204);
            }
            break;

        default:
            http_response_code(405);
            echo json_encode(["error" => "Method not allowed"]);
    }
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(["error" => "Database error: " . $e->getMessage()]);
}
