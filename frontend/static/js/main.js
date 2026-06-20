/**
 * NUTRACKER FRONTEND
 * SPA для работы с API трекера питания
 */

// ============================================================
// API CLIENT
// ============================================================

const API = {
    async get(endpoint) {
        const res = await fetch(`/api${endpoint}`);
        if (!res.ok) throw new Error(`API error: ${res.status}`);
        return res.json();
    },

    async post(endpoint, data) {
        const res = await fetch(`/api${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!res.ok) throw new Error(`API error: ${res.status}`);
        return res.json();
    },

    async delete(endpoint) {
        const res = await fetch(`/api${endpoint}`, { method: 'DELETE' });
        if (!res.ok) throw new Error(`API error: ${res.status}`);
        return res.json();
    }
};

// ============================================================
// UI RENDERERS
// ============================================================

function renderStatus(status, message) {
    const el = document.querySelector('#api-status .status-text');
    if (el) {
        el.textContent = status === 'ok' ? `✓ ${message}` : `✗ ${message}`;
        el.style.color = status === 'ok' ? '#22c55e' : '#ef4444';
    }
}

function renderProducts(products) {
    const container = document.getElementById('products-list');
    if (!container) return;

    if (!products || products.length === 0) {
        container.innerHTML = '<p class="empty">Нет продуктов</p>';
        return;
    }

    container.innerHTML = `
        <table class="products-table">
            <thead>
                <tr>
                    <th>Название</th>
                    <th>Ккал</th>
                    <th>Белки</th>
                    <th>Углеводы</th>
                    <th>Жиры</th>
                    <th>Действия</th>
                </tr>
            </thead>
            <tbody>
                ${products.map(p => `
                    <tr>
                        <td>${p.product_name || p.name || '—'}</td>
                        <td>${p.product_calories ?? p.calories ?? '—'}</td>
                        <td>${p.product_proteins ?? p.proteins ?? '—'}</td>
                        <td>${p.product_carbs ?? p.carbs ?? '—'}</td>
                        <td>${p.product_fats ?? p.fats ?? '—'}</td>
                        <td><button class="btn-delete" data-id="${p.id || p.product_id || ''}">✕</button></td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;

    // Навешиваем обработчики удаления
    container.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const id = e.target.dataset.id;
            if (confirm('Удалить продукт?')) {
                await deleteProduct(id);
            }
        });
    });
}

function renderDailySummary(summary) {
    const ids = ['today-calories', 'today-proteins', 'today-carbs', 'today-fats'];
    const keys = ['calories', 'proteins', 'carbs', 'fats'];

    ids.forEach((id, i) => {
        const el = document.getElementById(id);
        if (el) el.textContent = summary[keys[i]] ?? 0;
    });
}

// ============================================================
// ACTIONS
// ============================================================

async function loadProducts() {
    try {
        const products = await API.get('/products');
        renderProducts(products);
    } catch (err) {
        console.error('Failed to load products:', err);
        renderProducts([]);
    }
}

async function addProduct(data) {
    try {
        await API.post('/products', data);
        await loadProducts(); // Перезагружаем список
    } catch (err) {
        alert('Ошибка при добавлении продукта: ' + err.message);
    }
}

async function deleteProduct(id) {
    try {
        await API.delete(`/products/${id}`);
        await loadProducts();
    } catch (err) {
        alert('Ошибка при удалении: ' + err.message);
    }
}

async function checkStatus() {
    try {
        const data = await API.get('/status');
        renderStatus(data.status, data.message);
    } catch (err) {
        renderStatus('error', 'API недоступен');
    }
}

// ============================================================
// INITIALIZATION
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('Nutracker frontend loaded');

    // Проверка статуса API
    checkStatus();

    // Загрузка продуктов
    loadProducts();

    // Обработчик формы добавления продукта
    const form = document.getElementById('add-product-form');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const productData = {
                name: document.getElementById('product-name').value,
                calories: parseFloat(document.getElementById('product-calories').value),
                proteins: parseFloat(document.getElementById('product-proteins').value),
                carbs: parseFloat(document.getElementById('product-carbs').value),
                fats: parseFloat(document.getElementById('product-fats').value)
            };

            await addProduct(productData);
            form.reset();
        });
    }
});