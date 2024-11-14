
document.addEventListener('DOMContentLoaded', function() {
    // API status kontrolü
    async function checkApiStatus() {
        try {
            const response = await fetch('/health');
            const data = await response.json();
            
            const statusElement = document.getElementById('api-status');
            if (statusElement) {
                if (data.status === 'healthy') {
                    statusElement.textContent = 'API Durumu: Aktif';
                    statusElement.style.color = 'green';
                } else {
                    statusElement.textContent = 'API Durumu: Pasif';
                    statusElement.style.color = 'red';
                }
            }
        } catch (error) {
            console.error('API durum kontrolü başarısız:', error);
        }
    }

    // Sayfa yüklendiğinde API durumunu kontrol et
    checkApiStatus();

    // Her 30 saniyede bir API durumunu kontrol et
    setInterval(checkApiStatus, 30000);
});
