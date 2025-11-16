// Основной JavaScript файл для фронтенда
console.log('Frontend JS loaded');

// Функция для общения с API
async function fetchData(endpoint) {
    try {
        const response = await fetch(`/api/${endpoint}`);
        return await response.json();
    } catch (error) {
        console.error('Ошибка при загрузке данных:', error);
        throw error;
    }
}

// Дополнительные функции для фронтенда...