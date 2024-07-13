document.addEventListener('DOMContentLoaded', function () {
        const serverTime = new Date("{{ server_time|date:'c' }}");
        const clientTime = new Date();
        const timeDifference = serverTime - clientTime;

        function updateTimes() {
            let now = new Date(new Date().getTime() + timeDifference);

            // Проверяем текущий день недели
            const dayOfWeek = now.getDay(); // 0 - Воскресенье, 1 - Понедельник, ..., 6 - Суббота

            // Если сегодня воскресенье (0) или понедельник (1), переключаемся на вторник (2)
            if (dayOfWeek === 0 || dayOfWeek === 1) {
                now.setDate(now.getDate() + ((2 - dayOfWeek) % 7));
            }

            const openingTime = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 8, 0, 0);
            const closingTime = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 19, 0, 0);

            let isLibraryOpen = now >= openingTime && now < closingTime;

            const openStatus = document.getElementById('library-status-open');
            const closeStatus = document.getElementById('library-status-close');

            document.getElementById('services-current-date').textContent = now.toLocaleDateString('ru-RU', {
                weekday: 'long',
                day: 'numeric',
                month: 'long'
            });

            // Обновление текущего времени
            document.getElementById('services-current-time').textContent = now.toLocaleTimeString('ru-RU', {
                hour: '2-digit',
                minute: '2-digit',
            });

            if (isLibraryOpen) {
                closeStatus.style.display = 'none';
                openStatus.style.display = 'block';
            } else {
                openStatus.style.display = 'none';
                closeStatus.style.display = 'block';
            }

            let msUntilChange = isLibraryOpen ? closingTime - now : now < openingTime ? openingTime - now : openingTime.setDate(openingTime.getDate() + 1) - now;
            const hours = Math.floor(msUntilChange / 3600000);
            const minutes = Math.floor((msUntilChange % 3600000) / 60000);
            const seconds = Math.floor((msUntilChange % 60000) / 1000);

            document.getElementById('services-close-time').textContent =
                `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }

        updateTimes();
        setInterval(updateTimes, 1000);
    });