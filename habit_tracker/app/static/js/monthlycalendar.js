/* ----------------------- CONFIG ----------------------- */

/* ----------------------- HELPERS ---------------------- */
const daysInMonth = (m, y) => new Date(y, m + 1, 0).getDate();

const pad = (n) => (n < 10 ? "0" + n : n);

// Build a unique localStorage key for a particular habit/day
const makeKey = (y, m, d, hIdx) => `${y}-${pad(m)}-${pad(d)}-${hIdx}`;

/* ----------------------- STATE ------------------------ */
let currentDate = new Date(); // Today (month-level navigation will mutate this)

/* ---------------------- RENDERING --------------------- */
function renderCalendar() {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    const totalDays = daysInMonth(month, year);

    // Header label
    const monthLabel = document.getElementById("monthLabel");
    monthLabel.textContent = currentDate.toLocaleString("default", {
        month: "long",
        year: "numeric",
    });

    // Table element
    const tbl = document.getElementById("calendar");
    tbl.innerHTML = ""; // Reset

    /* ----------------- Build table header ---------------- */
    const dowLabels = ["M", "T", "W", "T", "F", "S", "S"];

    let headerRow1 = "<tr><th></th>";
    let headerRow2 = "<tr><th></th>";

    for (let day = 1; day <= totalDays; day++) {
        headerRow1 += `<th>${day}</th>`;

        // JavaScript Date: 0 = Sunday, so adjust to make Monday first (0..6 -> 0..6)
        const dow = (new Date(year, month, day).getDay() + 6) % 7;
        headerRow2 += `<th>${dowLabels[dow]}</th>`;
    }

    headerRow1 += "</tr>";
    headerRow2 += "</tr>";
    tbl.insertAdjacentHTML("beforeend", `<thead>${headerRow1}${headerRow2}</thead>`);

    /* ----------------- Build table body ------------------ */
    let tbodyHtml = "<tbody>";

    habits.forEach((habit, hIdx) => {
        tbodyHtml += `<tr><th class="text-start">${habit.name}</th>`;
        for (let day = 1; day <= totalDays; day++) {
            const key = makeKey(year, month + 1, day, hIdx);

            const dateStr = `${year}-${pad(month + 1)}-${pad(day)}`;

            // ✅ Correct matching
            const completion = habitCompletions.find(hc => hc.habit_id === habit.id && hc.date === dateStr);

            // ✅ Debug only if a match is found
            if (completion) {
                console.log(`✅ Found Completion: Habit [${habit.name}] on [${dateStr}] Status: [${completion.status}]`);
            }

            let style = "";

            if (completion) {
                if (completion.status === "done") {
                    style = `style="background:${habit.color};"`;  // Completed habit ➔ use habit's color
                } else if (completion.status === "missed") {
                    style = `style="background:#f8d7da;"`; // Missed habit ➔ light red color
                }
            }

            tbodyHtml += `<td data-key="${key}" data-habit="${hIdx}" ${style}></td>`;
        }
        tbodyHtml += "</tr>";
    });

    tbodyHtml += "</tbody>";
    tbl.insertAdjacentHTML("beforeend", tbodyHtml);

    /* ---------------- Cell click handlers --------------- */
    tbl.querySelectorAll("td").forEach((cell) => {
        cell.addEventListener("click", () => {
            const key = cell.dataset.key;
            const hIdx = parseInt(cell.dataset.habit, 10);
            const habitColor = habits[hIdx].color || "#ccc";
    
            const wasDone = cell.classList.contains('completed');
    
            if (wasDone) {
                cell.style.backgroundColor = "";
                cell.classList.remove('completed');
                localStorage.removeItem(key);
            } else {
                cell.style.backgroundColor = habitColor;
                cell.classList.add('completed');
                localStorage.setItem(key, "1");
            }
        });
    });
    

/* ------------------ Navigation buttons ---------------- */
document.getElementById("prevMonth").addEventListener("click", () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar();
});

document.getElementById("nextMonth").addEventListener("click", () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar();
});

/* --------------- Share button placeholder -------------- */
document.getElementById("shareBtn").addEventListener("click", () => {
    // For now we simply alert; you can replace with image export / share logic
    alert("Share functionality coming soon! 🥳");
});

// Initial render on page load
renderCalendar();
