// Helpers
const daysInMonth = (m, y) => new Date(y, m + 1, 0).getDate();
const pad = (n) => (n < 10 ? "0" + n : n);
const makeKey = (y, m, d, hIdx) => `${y}-${pad(m)}-${pad(d)}-${hIdx}`;

// DOM Elements
const monthLabel = document.getElementById('monthLabel');
const calendarTable = document.getElementById('calendar');
const prevMonthBtn = document.getElementById('prevMonth');
const nextMonthBtn = document.getElementById('nextMonth');
const shareBtn = document.getElementById('shareBtn');
const todayBtn = document.getElementById('todayBtn');

// Calendar Rendering
function renderCalendar() {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    const today = new Date();

    // Update month label
    monthLabel.textContent = currentDate.toLocaleString('default', {
        month: 'long',
        year: 'numeric'
    });

    // Generate table structure
    calendarTable.innerHTML = generateTableHTML(year, month, today);

    // Add event listeners
    setupEventListeners();

    // Update stats
    updateStats();
}

function generateTableHTML(year, month, today) {
    const totalDays = daysInMonth(month, year);
    let html = '<thead><tr><th>Habits</th>';

    for (let day = 1; day <= totalDays; day++) {
        const date = new Date(year, month, day);
        html += `<th>${day}<div class="day-of-week">${getShortWeekday(date)}</div></th>`;
    }

    html += '</tr></thead><tbody>';

    habits.forEach((habit, hIdx) => {
        html += `<tr><th>${habit.name}</th>`;
        for (let day = 1; day <= totalDays; day++) {
            html += generateDayCell(year, month, day, hIdx, habit.color, today);
        }
        html += '</tr>';
    });

    return html + '</tbody>';
}

function generateDayCell(year, month, day, hIdx, color, today) {
    const key = makeKey(year, month + 1, day, hIdx);
    const done = localStorage.getItem(key) === "1";
    const isToday = isCurrentDay(year, month, day, today);

    let classes = [];
    if (done) classes.push('completed');
    if (isToday) classes.push('today');

    return `<td data-key="${key}" data-habit="${hIdx}"
            ${done ? `style="background:${color}"` : ''}
            ${classes.length ? `class="${classes.join(' ')}"` : ''}></td>`;
}

function getShortWeekday(date) {
    return ['S', 'M', 'T', 'W', 'T', 'F', 'S'][date.getDay()];
}

function isCurrentDay(year, month, day, today) {
    return year === today.getFullYear() &&
        month === today.getMonth() &&
        day === today.getDate();
}

function setupEventListeners() {
    calendarTable.querySelectorAll('td').forEach(cell => {
        cell.addEventListener('click', handleCellClick);
        cell.addEventListener('mouseenter', () => {
            if (!cell.classList.contains('completed')) {
                cell.style.backgroundColor = '#f8fafc';
            }
        });
        cell.addEventListener('mouseleave', () => {
            if (!cell.classList.contains('completed')) {
                cell.style.backgroundColor = '';
            }
        });
    });
}

function handleCellClick() {
    const key = this.dataset.key;
    const hIdx = parseInt(this.dataset.habit, 10);
    const habitColor = habits[hIdx].color;

    if (this.classList.contains('completed')) {
        this.style.backgroundColor = '';
        this.classList.remove('completed');
        localStorage.removeItem(key);
    } else {
        this.style.backgroundColor = habitColor;
        this.classList.add('completed');
        localStorage.setItem(key, "1");

        this.style.transform = 'scale(0.95)';
        setTimeout(() => {
            this.style.transform = '';
        }, 200);
    }

    updateStats();  // Live update after each click
}

function updateStats() {
    const allCells = calendarTable.querySelectorAll('td[data-key]');
    const completed = [...allCells].filter(td => td.classList.contains('completed')).length;
    const total = allCells.length;
    const rate = total ? Math.round((completed / total) * 100) : 0;

    document.getElementById('completedDays').textContent = completed;
    document.getElementById('completionRate').textContent = rate + '%';
    document.getElementById('currentStreak').textContent = 0;
}

// Navigation
prevMonthBtn.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar();
});

nextMonthBtn.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar();
});

todayBtn.addEventListener('click', () => {
    currentDate = new Date();
    renderCalendar();
});

// Share Button
shareBtn.addEventListener('click', async () => {
    shareBtn.disabled = true;
    shareBtn.textContent = 'Generating...';

    try {
        await new Promise(resolve => setTimeout(resolve, 800));
        alert('Share functionality coming in next update!');
    } finally {
        shareBtn.disabled = false;
        shareBtn.textContent = 'Share';
    }
});

// Initial Render
document.addEventListener('DOMContentLoaded', renderCalendar);
