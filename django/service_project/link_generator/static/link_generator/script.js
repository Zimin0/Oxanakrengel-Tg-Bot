document.getElementById('generate-button').addEventListener('click', function() {
    const inputLink = document.getElementById('input-link').value.trim(); // Убираем пробелы по краям

    // Проверяем, что поле не пустое и не содержит 'http'
    if (!inputLink) {
        alert("Пожалуйста, введите ссылку на товар.");
        return; // Прекращаем выполнение функции
    } else if (!inputLink.includes('http')) {
        alert("Введенная ссылка должна содержать 'http'. Введите, пожалуйста, ссылку целиком, с 'http' или 'https'.");
        return; // Прекращаем выполнение функции
    }

    try {
        const generatedLink = getBotLinkWithArg(inputLink);
        document.getElementById('generated-link').href = generatedLink;
        document.getElementById('generated-link').textContent = generatedLink;
        document.getElementById('copy-button').style.display = 'inline-block'; // Показать кнопку копирования
    } catch (error) {
        alert(error.message);
    }
});


document.getElementById('copy-button').addEventListener('click', function() {
    const link = document.getElementById('generated-link').href;
    navigator.clipboard.writeText(link).then(() => {
        const button = document.getElementById('copy-button');
        button.textContent = 'Скопировано!';
        setTimeout(() => button.textContent = 'Копировать', 2000); // Сбросить текст кнопки через 2 секунды
    });
});


const MAX_TELEGRAM_ARG_LENGTH = 64;
const BOT_NAME = 'OxanaKrengelShopBot';

function getBotLinkWithArg(productUrl) {
    const productName = productUrl.split('/').pop();
    if (productName.length > MAX_TELEGRAM_ARG_LENGTH) {
        throw new Error("Длина ссылки на товар получается больше максимально доступной в телеграмм!");
    }
    const botLink = `https://t.me/${BOT_NAME}?start=${productName}`;
    return botLink;
}

