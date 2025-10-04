// Admin functions for managing coffee items

let editingId = null;

// Load coffee items for admin view
async function loadCoffeeItems() {
    try {
        const response = await fetch('/api/coffees');
        const items = await response.json();
        displayCoffeeList(items);
    } catch (error) {
        console.error('Error loading coffee items:', error);
        alert('Error loading coffee items: ' + error.message);
    }
}

// Display coffee items in admin list
function displayCoffeeList(items) {
    const coffeeList = document.getElementById('coffeeList');
    coffeeList.innerHTML = '';
    
    items.forEach(item => {
        const coffeeItem = document.createElement('div');
        coffeeItem.className = 'coffee-item';
        coffeeItem.innerHTML = `
            <h3>${item.name}</h3>
            <p><strong>Category:</strong> ${item.category}</p>
            <p><strong>Description:</strong> ${item.description}</p>
            <p><strong>Price:</strong> ${item.price.toLocaleString('vi-VN')}đ</p>
            <p><strong>Available:</strong> ${item.available ? 'Yes' : 'No'}</p>
            <div>
                <button class="btn-edit" onclick="editCoffee(${item.id})">Edit</button>
                <button class="btn-delete" onclick="deleteCoffee(${item.id})">Delete</button>
            </div>
        `;
        coffeeList.appendChild(coffeeItem);
    });
}

// Handle form submission
async function handleFormSubmit(event) {
    event.preventDefault();
    
    const formData = {
        name: document.getElementById('coffeeName').value,
        description: document.getElementById('coffeeDescription').value,
        price: parseFloat(document.getElementById('coffeePrice').value),
        category: document.getElementById('coffeeCategory').value,
        available: document.getElementById('coffeeAvailable').checked
    };
    
    try {
        let response;
        if (editingId) {
            // Update existing item
            response = await fetch(`/api/coffees/${editingId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
        } else {
            // Create new item
            response = await fetch('/api/coffees', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
        }
        
        if (response.ok) {
            alert(editingId ? 'Coffee updated successfully!' : 'Coffee added successfully!');
            resetForm();
            loadCoffeeItems();
        } else {
            const errorText = await response.text();
            alert('Error: ' + errorText);
        }
    } catch (error) {
        console.error('Error submitting form:', error);
        alert('Error submitting form: ' + error.message);
    }
}

// Edit coffee item
async function editCoffee(id) {
    try {
        const response = await fetch(`/api/coffees/${id}`);
        const item = await response.json();
        
        // Fill form with item data
        document.getElementById('coffeeName').value = item.name;
        document.getElementById('coffeeDescription').value = item.description;
        document.getElementById('coffeePrice').value = item.price;
        document.getElementById('coffeeCategory').value = item.category;
        document.getElementById('coffeeAvailable').checked = item.available;
        
        editingId = id;
        document.querySelector('button[type="submit"]').textContent = 'Update Coffee';
    } catch (error) {
        console.error('Error loading coffee for edit:', error);
        alert('Error loading coffee for edit: ' + error.message);
    }
}

// Delete coffee item
async function deleteCoffee(id) {
    if (confirm('Are you sure you want to delete this coffee item?')) {
        try {
            const response = await fetch(`/api/coffees/${id}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                alert('Coffee deleted successfully!');
                loadCoffeeItems();
            } else {
                alert('Error deleting coffee');
            }
        } catch (error) {
            console.error('Error deleting coffee:', error);
            alert('Error deleting coffee: ' + error.message);
        }
    }
}

// Reset form
function resetForm() {
    document.getElementById('coffeeForm').reset();
    editingId = null;
    document.querySelector('button[type="submit"]').textContent = 'Add Coffee';
}

// Initialize admin page
document.addEventListener('DOMContentLoaded', function() {
    // Load coffee items
    loadCoffeeItems();
    
    // Add form submit handler
    document.getElementById('coffeeForm').addEventListener('submit', handleFormSubmit);
    
    console.log('Admin page initialized');
});
