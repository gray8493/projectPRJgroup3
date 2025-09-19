const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');
const path = require('path');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Serve static files (except index.html)
app.use(express.static(__dirname, {
    index: false // Disable automatic index.html serving
}));

// Database connection
const dbConfig = {
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 3306,
    user: process.env.DB_USER || 'root',
    password: process.env.DB_PASSWORD || 'anhthi060105',
    database: process.env.DB_NAME || 'cafe_pos',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
};

const pool = mysql.createPool(dbConfig);

// JWT Secret (in production, use environment variable)
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key';

// Authentication middleware
const authenticateToken = (req, res, next) => {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];

    if (!token) {
        return res.status(401).json({ error: 'Access token required' });
    }

    jwt.verify(token, JWT_SECRET, (err, user) => {
        if (err) {
            return res.status(403).json({ error: 'Invalid or expired token' });
        }
        req.user = user;
        next();
    });
};

// Login endpoint
app.post('/api/login', async (req, res) => {
    try {
        const { username, password } = req.body;
        
        if (!username || !password) {
            return res.status(400).json({ error: 'Username and password are required' });
        }
        
        // For demo purposes, use simple password check
        // In production, use bcrypt to hash passwords
        if (username === 'admin' && password === 'admin123') {
            const user = { id: 1, username: 'admin', name: 'Quản trị viên', role: 'admin' };
            const token = jwt.sign(user, JWT_SECRET, { expiresIn: '24h' });
            return res.json({ user, token });
        } else if (username === 'staff' && password === 'staff123') {
            const user = { id: 2, username: 'staff', name: 'Nhân viên', role: 'staff' };
            const token = jwt.sign(user, JWT_SECRET, { expiresIn: '24h' });
            return res.json({ user, token });
        } else {
            return res.status(401).json({ error: 'Invalid credentials' });
        }
    } catch (err) {
        console.error('Login error:', err);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Health check
app.get('/api/health', async (req, res) => {
    try {
        const [rows] = await pool.query('SELECT 1 AS ok');
        res.json({ ok: true, db: rows[0].ok === 1 });
    } catch (err) {
        res.status(500).json({ ok: false, error: err.message });
    }
});

// Get menu items (protected)
app.get('/api/menu', authenticateToken, async (req, res) => {
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

// Create menu item (admin only)
app.post('/api/menu', authenticateToken, async (req, res) => {
    try {
        // Check if user is admin
        if (req.user.role !== 'admin') {
            return res.status(403).json({ error: 'Admin access required' });
        }
        
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

// Update menu item (admin only)
app.put('/api/menu/:id', authenticateToken, async (req, res) => {
    try {
        // Check if user is admin
        if (req.user.role !== 'admin') {
            return res.status(403).json({ error: 'Admin access required' });
        }
        
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

// Delete menu item (admin only)
app.delete('/api/menu/:id', authenticateToken, async (req, res) => {
    try {
        // Check if user is admin
        if (req.user.role !== 'admin') {
            return res.status(403).json({ error: 'Admin access required' });
        }
        
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
    res.sendFile(path.join(__dirname, 'login.html'));
});

// Redirect old index.html to login
app.get('/index.html', (req, res) => {
    res.redirect('/');
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
