const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(__dirname));

// Database connection
const dbConfig = {
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 3306,
    user: process.env.DB_USER || 'root',
    password: process.env.DB_PASSWORD || '',
    database: process.env.DB_NAME || 'cafe_pos',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
};

const pool = mysql.createPool(dbConfig);

// Health check
app.get('/api/health', async (req, res) => {
    try {
        const [rows] = await pool.query('SELECT 1 AS ok');
        res.json({ ok: true, db: rows[0].ok === 1 });
    } catch (err) {
        res.status(500).json({ ok: false, error: err.message });
    }
});

// Get menu items
app.get('/api/menu', async (req, res) => {
    try {
        const { category } = req.query;
        let sql = 'SELECT id, name, price, category FROM menu_items';
        const params = [];
        
        if (category) {
            sql += ' WHERE category = ?';
            params.push(category);
        }
        
        sql += ' ORDER BY id ASC';
        const [rows] = await pool.query(sql, params);
        res.json(rows);
    } catch (err) {
        console.error('Database error:', err);
        res.status(500).json({ error: err.message });
    }
});

// Create menu item
app.post('/api/menu', async (req, res) => {
    try {
        const { name, price, category } = req.body;
        
        if (!name || price == null || !category) {
            return res.status(400).json({ error: 'name, price, category are required' });
        }
        
        const [result] = await pool.query(
            'INSERT INTO menu_items (name, price, category) VALUES (?, ?, ?)',
            [name, price, category]
        );
        
        const [rows] = await pool.query(
            'SELECT id, name, price, category FROM menu_items WHERE id = ?',
            [result.insertId]
        );
        
        res.status(201).json(rows[0]);
    } catch (err) {
        console.error('Database error:', err);
        res.status(500).json({ error: err.message });
    }
});

// Update menu item
app.put('/api/menu/:id', async (req, res) => {
    try {
        const { id } = req.params;
        const { name, price, category } = req.body;
        
        // Check if item exists
        const [existing] = await pool.query('SELECT id FROM menu_items WHERE id = ?', [id]);
        if (existing.length === 0) {
            return res.status(404).json({ error: 'Item not found' });
        }
        
        // Build update query
        const fields = [];
        const params = [];
        
        if (name !== undefined) { fields.push('name = ?'); params.push(name); }
        if (price !== undefined) { fields.push('price = ?'); params.push(price); }
        if (category !== undefined) { fields.push('category = ?'); params.push(category); }
        
        if (fields.length === 0) {
            return res.status(400).json({ error: 'No fields to update' });
        }
        
        params.push(id);
        await pool.query(
            `UPDATE menu_items SET ${fields.join(', ')}, updated_at = CURRENT_TIMESTAMP WHERE id = ?`,
            params
        );
        
        const [rows] = await pool.query(
            'SELECT id, name, price, category FROM menu_items WHERE id = ?',
            [id]
        );
        
        res.json(rows[0]);
    } catch (err) {
        console.error('Database error:', err);
        res.status(500).json({ error: err.message });
    }
});

// Delete menu item
app.delete('/api/menu/:id', async (req, res) => {
    try {
        const { id } = req.params;
        
        const [result] = await pool.query('DELETE FROM menu_items WHERE id = ?', [id]);
        
        if (result.affectedRows === 0) {
            return res.status(404).json({ error: 'Item not found' });
        }
        
        res.status(204).send();
    } catch (err) {
        console.error('Database error:', err);
        res.status(500).json({ error: err.message });
    }
});

// Serve static files
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Start server
app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
    console.log(`API endpoints:`);
    console.log(`  GET  /api/health - Health check`);
    console.log(`  GET  /api/menu - Get all menu items`);
    console.log(`  GET  /api/menu?category=coffee - Get items by category`);
    console.log(`  POST /api/menu - Create new item`);
    console.log(`  PUT  /api/menu/:id - Update item`);
    console.log(`  DELETE /api/menu/:id - Delete item`);
});
