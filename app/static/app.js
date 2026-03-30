/**
 * Keep the dashboard state in one place so all panels stay in sync.
 */
const state = {
    subscribers: [],
    currentDevices: [],
    selectedUserId: null,
    selectedDeviceId: null,
    usageChart: null,
};

/**
 * Map status values to badge styles defined in the CSS theme.
 *
 * @param {string} value - Status string from the API response.
 * @returns {string} CSS class list for the badge.
 */
function badgeClass(value) {
    const normalizedValue = (value || "").toLowerCase();

    if (["active", "online", "normal"].includes(normalizedValue)) {
        return "badge status-active";
    }

    if (["paused", "standby"].includes(normalizedValue)) {
        return "badge status-paused";
    }

    if (["expired", "error", "warning"].includes(normalizedValue)) {
        return "badge status-expired";
    }

    if (normalizedValue === "offline") {
        return "badge status-offline";
    }

    if (["on", "cleaning"].includes(normalizedValue)) {
        return "badge status-on";
    }

    if (normalizedValue === "off") {
        return "badge status-off";
    }

    return "badge";
}

/**
 * Wrap raw status text with the correct badge markup.
 *
 * @param {string} value - Status string shown to the user.
 * @returns {string} HTML string for the badge element.
 */
function badgeMarkup(value) {
    return `<span class="${badgeClass(value)}">${value}</span>`;
}

/**
 * Fetch JSON and normalize API-level errors into JavaScript exceptions.
 *
 * @param {string} url - API endpoint to request.
 * @returns {Promise<object>} Parsed response body.
 */
async function fetchJson(url) {
    const response = await fetch(url);
    const payload = await response.json();

    if (!response.ok) {
        throw new Error(payload.error?.message || "Request failed.");
    }

    return payload;
}

/**
 * Find the currently selected subscriber model for helper labels.
 *
 * @returns {object|null} The selected subscriber or null.
 */
function selectedSubscriber() {
    return state.subscribers.find((subscriber) => subscriber.userId === state.selectedUserId) || null;
}

/**
 * Render the four summary cards above the tables.
 */
function renderSummary() {
    const activeCount = state.subscribers.filter((subscriber) => subscriber.status === "Active").length;
    const inactiveCount = state.subscribers.filter((subscriber) => subscriber.status !== "Active").length;
    const totalDevices = state.subscribers.reduce((total, subscriber) => total + subscriber.deviceCount, 0);

    document.getElementById("summary-total").textContent = String(state.subscribers.length);
    document.getElementById("summary-active").textContent = String(activeCount);
    document.getElementById("summary-inactive").textContent = String(inactiveCount);
    document.getElementById("summary-devices").textContent = String(totalDevices);
}

/**
 * Reset the usage panel when the subscriber or selected device changes.
 *
 * @param {string} message - Empty-state message to show.
 */
function resetUsagePanel(message) {
    const emptyElement = document.getElementById("usage-empty");
    const detailElement = document.getElementById("usage-detail");
    const infoElement = document.getElementById("usage-info");
    const highlightElement = document.getElementById("usage-highlight");

    emptyElement.textContent = message;
    emptyElement.classList.remove("hidden");
    detailElement.classList.add("hidden");
    infoElement.innerHTML = "";
    highlightElement.innerHTML = "";

    if (state.usageChart) {
        state.usageChart.destroy();
        state.usageChart = null;
    }
}

/**
 * Load subscribers on first page entry as required by the specification.
 */
async function fetchSubscribers() {
    const emptyElement = document.getElementById("subscriber-empty");

    try {
        emptyElement.textContent = "구독자 정보를 불러오는 중입니다.";
        emptyElement.classList.remove("hidden");

        const payload = await fetchJson("/api/v1/subscribers");
        state.subscribers = payload.data;
        renderSummary();
        renderSubscribers();
    } catch (error) {
        emptyElement.textContent = error.message;
    }
}

/**
 * Render the subscriber table with real-time search and status filters.
 */
function renderSubscribers() {
    const emptyElement = document.getElementById("subscriber-empty");
    const tbody = document.getElementById("subscriber-body");
    const searchKeyword = document.getElementById("subscriber-search").value.trim().toLowerCase();
    const statusFilter = document.getElementById("subscriber-status-filter").value;

    const filteredSubscribers = state.subscribers.filter((subscriber) => {
        const matchesSearch = [
            subscriber.userId,
            subscriber.name,
            subscriber.plan,
            subscriber.status,
        ]
            .join(" ")
            .toLowerCase()
            .includes(searchKeyword);

        const matchesStatus = !statusFilter || subscriber.status === statusFilter;
        return matchesSearch && matchesStatus;
    });

    tbody.innerHTML = filteredSubscribers
        .map(
            (subscriber) => `
                <tr
                    class="clickable ${state.selectedUserId === subscriber.userId ? "selected" : ""}"
                    data-user-id="${subscriber.userId}"
                >
                    <td>${subscriber.userId}</td>
                    <td class="name-cell">
                        <strong>${subscriber.name}</strong>
                        <span>${subscriber.organization}</span>
                    </td>
                    <td>${subscriber.plan}</td>
                    <td>${badgeMarkup(subscriber.status)}</td>
                    <td>${subscriber.deviceCount}</td>
                </tr>
            `,
        )
        .join("");

    if (filteredSubscribers.length === 0) {
        emptyElement.textContent = "조건에 맞는 구독자가 없습니다.";
        emptyElement.classList.remove("hidden");
    } else {
        emptyElement.classList.add("hidden");
    }

    tbody.querySelectorAll("tr").forEach((row) => {
        row.addEventListener("click", () => selectSubscriber(row.dataset.userId));
    });
}

/**
 * Load the selected subscriber's devices and reset the usage detail area.
 *
 * @param {string} userId - Subscriber identifier selected in the table.
 */
async function selectSubscriber(userId) {
    state.selectedUserId = userId;
    state.selectedDeviceId = null;
    state.currentDevices = [];
    renderSubscribers();
    resetUsagePanel("가전을 선택하면 상세 사용 현황과 주간 Bar Chart가 표시됩니다.");

    const emptyElement = document.getElementById("device-empty");
    const tableElement = document.getElementById("device-table");
    emptyElement.textContent = "선택한 사용자의 가전 목록을 불러오는 중입니다.";
    emptyElement.classList.remove("hidden");
    tableElement.classList.add("hidden");

    try {
        const payload = await fetchJson(`/api/v1/subscribers/${userId}/devices`);
        state.currentDevices = payload.data;
        renderDevices();
    } catch (error) {
        emptyElement.textContent = error.message;
    }
}

/**
 * Render the selected subscriber's device table with live filtering.
 */
function renderDevices() {
    const emptyElement = document.getElementById("device-empty");
    const tableElement = document.getElementById("device-table");
    const tbody = document.getElementById("device-body");
    const searchKeyword = document.getElementById("device-search").value.trim().toLowerCase();
    const statusFilter = document.getElementById("device-status-filter").value;

    if (!state.selectedUserId) {
        tbody.innerHTML = "";
        tableElement.classList.add("hidden");
        emptyElement.textContent = "구독자를 선택하면 가전 목록이 표시됩니다.";
        emptyElement.classList.remove("hidden");
        return;
    }

    const filteredDevices = state.currentDevices.filter((device) => {
        const matchesSearch = [
            device.deviceId,
            device.type,
            device.model,
            device.location,
            device.status,
        ]
            .join(" ")
            .toLowerCase()
            .includes(searchKeyword);

        const matchesStatus = !statusFilter || device.status === statusFilter;
        return matchesSearch && matchesStatus;
    });

    tbody.innerHTML = filteredDevices
        .map(
            (device) => `
                <tr
                    class="clickable ${state.selectedDeviceId === device.deviceId ? "selected" : ""}"
                    data-device-id="${device.deviceId}"
                >
                    <td>${device.deviceId}</td>
                    <td>${device.type}</td>
                    <td class="name-cell">
                        <strong>${device.model}</strong>
                        <span>Last seen ${device.lastSeen}</span>
                    </td>
                    <td>${device.location}</td>
                    <td>${badgeMarkup(device.status)}</td>
                </tr>
            `,
        )
        .join("");

    if (state.currentDevices.length === 0) {
        tableElement.classList.add("hidden");
        emptyElement.textContent = "No registered devices.";
        emptyElement.classList.remove("hidden");
        return;
    }

    if (filteredDevices.length === 0) {
        tableElement.classList.add("hidden");
        emptyElement.textContent = "No devices matched your filter.";
        emptyElement.classList.remove("hidden");
        return;
    }

    tableElement.classList.remove("hidden");
    emptyElement.classList.add("hidden");

    tbody.querySelectorAll("tr").forEach((row) => {
        row.addEventListener("click", () => selectDevice(row.dataset.deviceId));
    });
}

/**
 * Render the selected device's detail cards and highlight summary.
 *
 * @param {object} usage - Usage detail payload from the API.
 */
function renderUsageDetails(usage) {
    const emptyElement = document.getElementById("usage-empty");
    const detailElement = document.getElementById("usage-detail");
    const infoElement = document.getElementById("usage-info");
    const highlightElement = document.getElementById("usage-highlight");
    const subscriber = selectedSubscriber();

    highlightElement.innerHTML = `
        <strong>${usage.deviceName}</strong>
        <span>${subscriber ? `${subscriber.name}님의 ${usage.deviceId}` : usage.deviceId}</span>
        <p class="subtle">${usage.remark}</p>
    `;

    const detailItems = [
        ["Device ID", usage.deviceId],
        ["Device Name", usage.deviceName],
        ["Power Status", badgeMarkup(usage.powerStatus)],
        ["Last Used", usage.lastUsedAt],
        ["Total Usage Hours", `${usage.totalUsageHours} hours`],
        ["Weekly Usage Count", `${usage.weeklyUsageCount} times`],
        ["Health Status", badgeMarkup(usage.healthStatus)],
        ["Remark", usage.remark],
    ];

    infoElement.innerHTML = detailItems
        .map(
            ([label, value]) => `
                <article class="detail-item">
                    <span class="label">${label}</span>
                    <div class="value">${value}</div>
                </article>
            `,
        )
        .join("");

    emptyElement.classList.add("hidden");
    detailElement.classList.remove("hidden");
}

/**
 * Load the selected device's usage payload and draw the weekly trend chart.
 *
 * @param {string} deviceId - Device identifier selected in the table.
 */
async function selectDevice(deviceId) {
    state.selectedDeviceId = deviceId;
    renderDevices();
    resetUsagePanel("상세 사용 현황을 불러오는 중입니다.");

    try {
        const payload = await fetchJson(`/api/v1/devices/${deviceId}/usage`);
        renderUsageDetails(payload.data);
        renderUsageChart(payload.data.weeklyUsageTrend);
    } catch (error) {
        resetUsagePanel(error.message);
    }
}

/**
 * Draw the weekly usage Bar Chart required by the specification.
 *
 * @param {number[]} trend - Daily usage values from Monday to Sunday.
 */
function renderUsageChart(trend) {
    const context = document.getElementById("usageChart");

    if (state.usageChart) {
        state.usageChart.destroy();
    }

    state.usageChart = new Chart(context, {
        type: "bar",
        data: {
            labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            datasets: [
                {
                    label: "Usage Count",
                    data: trend,
                    backgroundColor: [
                        "#7EB6FF",
                        "#63A1FF",
                        "#4B8DFF",
                        "#3182F6",
                        "#2C74DE",
                        "#245FBD",
                        "#1E4E9B",
                    ],
                    borderRadius: 12,
                    borderSkipped: false,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            resizeDelay: 150,
            animation: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                    },
                    grid: {
                        color: "rgba(148, 163, 184, 0.18)",
                    },
                },
                x: {
                    grid: {
                        display: false,
                    },
                },
            },
            plugins: {
                legend: {
                    display: false,
                },
                tooltip: {
                    animation: false,
                },
            },
        },
    });
}

/**
 * Bind input events so search and filters react immediately.
 */
function bindEvents() {
    document.getElementById("subscriber-search").addEventListener("input", renderSubscribers);
    document.getElementById("subscriber-status-filter").addEventListener("change", renderSubscribers);
    document.getElementById("device-search").addEventListener("input", renderDevices);
    document.getElementById("device-status-filter").addEventListener("change", renderDevices);
}

document.addEventListener("DOMContentLoaded", () => {
    bindEvents();
    resetUsagePanel("가전을 선택하면 상세 사용 현황과 주간 Bar Chart가 표시됩니다.");

    if (window.lucide) {
        window.lucide.createIcons();
    }

    fetchSubscribers();
});
