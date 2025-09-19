
        // API configuration - Node.js Express server
        const API_BASE = '/api';

        let cart = [];
        let currentOrderType = 'dine-in';
        let selectedTable = null;
        let currentCategory = 'coffee';

        // Initialize the application
        async function init() {
            updateTime();
            setInterval(updateTime, 1000);
            generateTables();
            await loadProducts('coffee');
            await renderMenuList('coffee');
            setupEventListeners();
        }

        // Update current time
        function updateTime() {
            const now = new Date();
            const timeString = now.toLocaleTimeString('vi-VN');
            document.getElementById('current-time').textContent = timeString;
        }

        // Generate table buttons
        function generateTables() {
            const tableGrid = document.getElementById('table-grid');
            tableGrid.innerHTML = '';
            
            for (let i = 1; i <= 12; i++) {
                const tableBtn = document.createElement('button');
                tableBtn.className = 'table-btn';
                tableBtn.textContent = `Bàn ${i}`;
                tableBtn.onclick = () => selectTable(i);
                tableGrid.appendChild(tableBtn);
            }
        }

        // Select table
        function selectTable(tableNumber) {
            const tables = document.querySelectorAll('.table-btn');
            tables.forEach(table => table.classList.remove('selected'));
            
            event.target.classList.add('selected');
            selectedTable = tableNumber;
        }

        // Setup event listeners
        function setupEventListeners() {
            // Order type buttons
            document.querySelectorAll('.order-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    document.querySelectorAll('.order-btn').forEach(b => b.classList.remove('active'));
                    e.target.classList.add('active');
                    currentOrderType = e.target.dataset.type;
                    
                    // Show/hide table selection
                    const tableSelection = document.getElementById('table-selection');
                    if (currentOrderType === 'dine-in') {
                        tableSelection.classList.remove('hidden');
                    } else {
                        tableSelection.classList.add('hidden');
                        selectedTable = null;
                    }
                });
            });

            // Category tabs
            document.querySelectorAll('.category-tab').forEach(tab => {
                tab.addEventListener('click', async (e) => {
                    document.querySelectorAll('.category-tab').forEach(t => t.classList.remove('active'));
                    e.target.classList.add('active');
                    currentCategory = e.target.dataset.category;
                    await loadProducts(currentCategory);
                    await renderMenuList(currentCategory);
                });
            });

            // Modal close
            document.querySelector('.close').addEventListener('click', () => {
                document.getElementById('checkout-modal').style.display = 'none';
            });

            window.addEventListener('click', (e) => {
                const modal = document.getElementById('checkout-modal');
                if (e.target === modal) {
                    modal.style.display = 'none';
                }
            });

            // Management handlers
            setupManagement();
        }

        // Load products by category
        async function loadProducts(category) {
            const grid = document.getElementById('products-grid');
            grid.innerHTML = '';

            // Prefer API data; fetchMenu already falls back to local sample if API fails
            const items = await fetchMenu(category);
            
            items.forEach(product => {
                const productCard = document.createElement('div');
                productCard.className = 'product-card';
                productCard.onclick = () => addToCart(product);

                productCard.innerHTML = `
                    <div class="product-image">
                        <i class="fas fa-coffee"></i>
                    </div>
                    <div class="product-name">${product.name}</div>
                    <div class="product-price">${formatPrice(Number(product.price))}</div>
                `;

                grid.appendChild(productCard);
            });
        }

        // Add item to cart
        function addToCart(product) {
            const existingItem = cart.find(item => item.id === product.id);
            
            if (existingItem) {
                existingItem.quantity += 1;
            } else {
                cart.push({...product, quantity: 1});
            }
            
            updateCartDisplay();
        }

        // Remove item from cart
        function removeFromCart(productId) {
            const itemIndex = cart.findIndex(item => item.id === productId);
            if (itemIndex > -1) {
                cart.splice(itemIndex, 1);
                updateCartDisplay();
            }
        }

        // Update item quantity
        function updateQuantity(productId, change) {
            const item = cart.find(item => item.id === productId);
            if (item) {
                item.quantity += change;
                if (item.quantity <= 0) {
                    removeFromCart(productId);
                } else {
                    updateCartDisplay();
                }
            }
        }

        // Update cart display
        function updateCartDisplay() {
            const cartItems = document.getElementById('cart-items');
            const cartCount = document.getElementById('cart-count');
            const totalAmount = document.getElementById('total-amount');

            cartItems.innerHTML = '';
            let total = 0;
            let itemCount = 0;

            cart.forEach(item => {
                const cartItem = document.createElement('div');
                cartItem.className = 'cart-item';
                
                const itemTotal = item.price * item.quantity;
                total += itemTotal;
                itemCount += item.quantity;

                cartItem.innerHTML = `
                    <div>
                        <div style="font-weight: bold;">${item.name}</div>
                        <div style="color: #666; font-size: 12px;">${formatPrice(item.price)} x ${item.quantity}</div>
                    </div>
                    <div class="quantity-controls">
                        <button class="qty-btn" onclick="updateQuantity(${item.id}, -1)">-</button>
                        <span>${item.quantity}</span>
                        <button class="qty-btn" onclick="updateQuantity(${item.id}, 1)">+</button>
                        <button class="qty-btn" onclick="removeFromCart(${item.id})" style="background: #dc3545; margin-left: 5px;">×</button>
                    </div>
                `;

                cartItems.appendChild(cartItem);
            });

            cartCount.textContent = `(${itemCount})`;
            totalAmount.textContent = formatPrice(total);
        }

        // Format price
        function formatPrice(price) {
            return new Intl.NumberFormat('vi-VN', {
                style: 'currency',
                currency: 'VND'
            }).format(price);
        }

        // Checkout function
        function checkout() {
            if (cart.length === 0) {
                alert('Vui lòng chọn ít nhất một món!');
                return;
            }

            if (currentOrderType === 'dine-in' && !selectedTable) {
                alert('Vui lòng chọn bàn!');
                return;
            }

            // Create order summary
            let orderSummary = `
                <h3>Chi tiết đơn hàng:</h3>
                <p><strong>Loại đơn:</strong> ${getOrderTypeName(currentOrderType)}</p>
            `;

            if (currentOrderType === 'dine-in') {
                orderSummary += `<p><strong>Bàn:</strong> ${selectedTable}</p>`;
            }

            orderSummary += '<h4>Món đã đặt:</h4><ul>';
            let total = 0;

            cart.forEach(item => {
                const itemTotal = item.price * item.quantity;
                total += itemTotal;
                orderSummary += `<li>${item.name} x${item.quantity} - ${formatPrice(itemTotal)}</li>`;
            });

            orderSummary += `</ul><h4>Tổng cộng: ${formatPrice(total)}</h4>`;

            document.getElementById('order-summary').innerHTML = orderSummary;
            document.getElementById('checkout-modal').style.display = 'block';

            // Save order to localStorage (thay thế bằng API call)
            const order = {
                id: Date.now(),
                type: currentOrderType,
                table: selectedTable,
                items: [...cart],
                total: total,
                timestamp: new Date().toISOString()
            };

            // Lưu vào localStorage (trong thực tế sẽ gửi lên server)
            const orders = JSON.parse(localStorage.getItem('orders') || '[]');
            orders.push(order);
            localStorage.setItem('orders', JSON.stringify(orders));

            // Clear cart
            cart = [];
            selectedTable = null;
            updateCartDisplay();
            
            // Reset selections
            document.querySelectorAll('.table-btn').forEach(btn => btn.classList.remove('selected'));
        }

        // Get order type name in Vietnamese
        function getOrderTypeName(type) {
            switch(type) {
                case 'dine-in': return 'Tại chỗ';
                case 'takeaway': return 'Mang về';
                case 'delivery': return 'Giao hàng';
                default: return type;
            }
        }

        // ---------- MENU MANAGEMENT (CRUD) ----------
        async function fetchMenu(category) {
            try {
                const res = await fetch(`${API_BASE}/menu?category=${encodeURIComponent(category)}&_=${Date.now()}` , { 
                    cache: 'no-store', 
                    headers: { 'Cache-Control': 'no-cache' } 
                });
                if (!res.ok) {
                    console.error('API Error:', res.status, res.statusText);
                    return [];
                }
                const data = await res.json();
                return Array.isArray(data) ? data : [];
            } catch (e) {
                console.error('API Error:', e);
                return [];
            }
        }

        async function renderMenuList(category) {
            const list = document.getElementById('menu-list');
            if (!list) return;
            list.innerHTML = '';
            const items = await fetchMenu(category);
            items.forEach(item => {
                const row = document.createElement('div');
                row.className = 'menu-item-row';
                row.innerHTML = `
                    <div>
                        <div style="font-weight: bold;">${item.name}</div>
                        <div style="color: #666;">${formatPrice(item.price)} · ${item.category}</div>
                    </div>
                    <div class="menu-actions">
                        <button class="btn" data-add="${item.id}">Thêm vào đơn</button>
                        <button class="btn" data-edit="${item.id}">Sửa</button>
                        <button class="btn" data-del="${item.id}">Xóa</button>
                    </div>
                `;
                const addBtn = row.querySelector('[data-add]');
                const editBtn = row.querySelector('[data-edit]');
                const delBtn = row.querySelector('[data-del]');
                if (addBtn) addBtn.addEventListener('click', () => addToCart(item));
                if (editBtn) editBtn.addEventListener('click', () => fillForm(item));
                if (delBtn) delBtn.addEventListener('click', () => deleteMenuItem(item.id));
                list.appendChild(row);
            });
        }

        function fillForm(item) {
            document.getElementById('menu-id').value = item.id || '';
            document.getElementById('menu-name').value = item.name || '';
            document.getElementById('menu-price').value = item.price || '';
            document.getElementById('menu-category').value = item.category || currentCategory;
        }

        function resetForm() {
            document.getElementById('menu-id').value = '';
            document.getElementById('menu-name').value = '';
            document.getElementById('menu-price').value = '';
            document.getElementById('menu-category').value = '';
        }

        async function createMenuItem(payload) {
            const res = await fetch(`${API_BASE}/menu`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (!res.ok) throw new Error(await res.text());
            return await res.json();
        }

        async function updateMenuItem(id, payload) {
            const res = await fetch(`${API_BASE}/menu/${encodeURIComponent(id)}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (!res.ok) throw new Error(await res.text());
            return await res.json();
        }

        async function deleteMenuItem(id) {
            if (!confirm('Xóa món này?')) return;
            const res = await fetch(`${API_BASE}/menu/${encodeURIComponent(id)}`, { method: 'DELETE' });
            if (!res.ok && res.status !== 204) { alert('Xóa thất bại: ' + (await res.text())); return; }
            await renderMenuList(currentCategory);
            await loadProducts(currentCategory);
        }

        function setupManagement() {
            const form = document.getElementById('menu-form');
            if (!form) return;
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                const id = document.getElementById('menu-id').value;
                const name = document.getElementById('menu-name').value.trim();
                const price = parseInt(document.getElementById('menu-price').value, 10) || 0;
                const category = document.getElementById('menu-category').value || currentCategory;
                if (!name || !category) return;
                try {
                    if (id) {
                        await updateMenuItem(id, { name, price, category });
                    } else {
                        await createMenuItem({ name, price, category });
                    }
                    resetForm();
                    await renderMenuList(currentCategory);
                    await loadProducts(currentCategory);
                } catch (err) {
                    alert('Lưu thất bại: ' + err);
                }
            });

            const resetBtn = document.getElementById('menu-reset-btn');
            if (resetBtn) resetBtn.addEventListener('click', (e) => { e.preventDefault(); resetForm(); });
        }

        // Initialize app when page loads
        document.addEventListener('DOMContentLoaded', init);
    