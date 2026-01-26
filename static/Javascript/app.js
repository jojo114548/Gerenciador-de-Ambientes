// Main application logic

const app = {
    currentTab: 'inicio',
    currentMonth: new Date(),
    currentBookingItem: null,
    currentBookingType: null,
    registeredEvents: new Set(),

    // Initialize the app
    init() {
        this.renderEvents();
        this.renderSpaces('spaces-grid-preview', 3);
        this.renderEquipment('equipment-grid-preview', 3);
        this.renderCalendar();
        this.renderUpcomingEvents();
        this.renderSpaces('spaces-grid-full');
        this.renderEquipment('equipment-grid-full');
        this.renderHistory();
        this.renderUsers();
        this.renderPendingBookings();
        this.setupFormValidation();
    },

    // Login/Logout
    showLoginModal() {
        document.getElementById('login-modal').classList.add('show');
    },

    hideLoginModal() {
        document.getElementById('login-modal').classList.remove('show');
    },

    handleLogin(event) {
        event.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        // Simple validation
        if (email && password) {
            this.hideLoginModal();
            document.getElementById('landing-page').style.display = 'none';
            document.getElementById('dashboard').style.display = 'flex';
            this.init();
        }
    },

    handleLogout(event) {
        event.preventDefault();
        if (confirm('Tem certeza que deseja sair?')) {
            document.getElementById('dashboard').style.display = 'none';
            document.getElementById('landing-page').style.display = 'block';
            document.getElementById('login-form').reset();
        }
    },

    // Tab Navigation
    switchTab(event, tabName) {
        event.preventDefault();
        
        // Update active tab
        this.currentTab = tabName;
        
        // Update nav items
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        event.currentTarget.classList.add('active');
        
        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`tab-${tabName}`).classList.add('active');
        
        // Show/hide calendar sidebar
        const calendarSidebar = document.getElementById('calendar-sidebar');
        if (tabName === 'inicio') {
            calendarSidebar.style.display = 'block';
        } else {
            calendarSidebar.style.display = 'none';
        }
    },

    // Render Events
    renderEvents() {
        const grid = document.getElementById('events-grid');
        grid.innerHTML = eventsData.map(event => this.createEventCard(event)).join('');
    },

    createEventCard(event) {
        const isRegistered = this.registeredEvents.has(event.id);
        const spotsLeft = event.capacity - event.attendees;
        
        return `
            <div class="event-card" onclick="app.showEventDetail(${event.id})">
                <div class="event-header">
                    <div class="event-date">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                            <line x1="16" y1="2" x2="16" y2="6"></line>
                            <line x1="8" y1="2" x2="8" y2="6"></line>
                            <line x1="3" y1="10" x2="21" y2="10"></line>
                        </svg>
                        ${this.formatDate(event.date)} às ${event.time}
                    </div>
                    <h3 class="event-title">${event.title}</h3>
                    <div class="event-location">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                            <circle cx="12" cy="10" r="3"></circle>
                        </svg>
                        ${event.location}
                    </div>
                </div>
                <div class="event-body">
                    <p class="event-description">${event.description}</p>
                    <div class="event-stats">
                        <div class="event-stat">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                                <circle cx="9" cy="7" r="4"></circle>
                                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                            </svg>
                            ${event.attendees}/${event.capacity} inscritos
                        </div>
                        <div class="event-stat">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <circle cx="12" cy="12" r="10"></circle>
                                <polyline points="12 6 12 12 16 14"></polyline>
                            </svg>
                            ${spotsLeft} vagas
                        </div>
                    </div>
                    <div class="event-actions" onclick="event.stopPropagation()">
                        ${isRegistered 
                            ? `<button class="btn-secondary" onclick="app.unregisterEvent(${event.id})">Cancelar Inscrição</button>`
                            : `<button class="btn-primary" onclick="app.registerEvent(${event.id})">Inscrever-se</button>`
                        }
                        <button class="btn-outline" onclick="app.showEventDetail(${event.id})">Ver Detalhes</button>
                    </div>
                </div>
            </div>
        `;
    },

    showEventDetail(eventId) {
        const event = eventsData.find(e => e.id === eventId);
        if (!event) return;

        const isRegistered = this.registeredEvents.has(eventId);
        const spotsLeft = event.capacity - event.attendees;

        const content = `
            <div class="detail-header">
                <img src="${event.image}" alt="${event.title}" class="detail-image">
                <div class="detail-title">
                    <h2>${event.title}</h2>
                    <span class="card-badge badge-purple">${event.type}</span>
                </div>
                <div class="detail-meta">
                    <div class="detail-meta-item">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                            <line x1="16" y1="2" x2="16" y2="6"></line>
                            <line x1="8" y1="2" x2="8" y2="6"></line>
                            <line x1="3" y1="10" x2="21" y2="10"></line>
                        </svg>
                        ${this.formatDate(event.date)}
                    </div>
                    <div class="detail-meta-item">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="10"></circle>
                            <polyline points="12 6 12 12 16 14"></polyline>
                        </svg>
                        ${event.time}
                    </div>
                    <div class="detail-meta-item">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                            <circle cx="12" cy="10" r="3"></circle>
                        </svg>
                        ${event.location}
                    </div>
                    <div class="detail-meta-item">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                            <circle cx="9" cy="7" r="4"></circle>
                            <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                        </svg>
                        ${event.attendees}/${event.capacity} participantes
                    </div>
                </div>
            </div>
            <div class="detail-section">
                <h3>Sobre o Evento</h3>
                <p>${event.description}</p>
            </div>
            <div class="detail-section">
                <h3>Informações Adicionais</h3>
                <div class="detail-meta">
                    <div class="detail-meta-item">
                        <strong>Instrutor:</strong> ${event.instructor}
                    </div>
                    <div class="detail-meta-item">
                        <strong>Vagas Restantes:</strong> ${spotsLeft}
                    </div>
                    <div class="detail-meta-item">
                        <strong>Tipo:</strong> ${event.type}
                    </div>
                </div>
            </div>
            <div class="detail-actions">
                ${isRegistered 
                    ? `<button class="btn-secondary btn-full" onclick="app.unregisterEvent(${eventId}); app.hideDetailModal()">Cancelar Inscrição</button>`
                    : `<button class="btn-primary btn-full" onclick="app.registerEvent(${eventId}); app.hideDetailModal()">Inscrever-se no Evento</button>`
                }
            </div>
        `;

        document.getElementById('detail-content').innerHTML = content;
        document.getElementById('detail-modal').classList.add('show');
    },

    registerEvent(eventId) {
        this.registeredEvents.add(eventId);
        this.renderEvents();
        alert('Inscrição realizada com sucesso!');
    },

    unregisterEvent(eventId) {
        if (confirm('Deseja realmente cancelar sua inscrição?')) {
            this.registeredEvents.delete(eventId);
            this.renderEvents();
            alert('Inscrição cancelada.');
        }
    },

    // Render Spaces
    renderSpaces(gridId, limit = null) {
        const grid = document.getElementById(gridId);
        const spaces = limit ? spacesData.slice(0, limit) : spacesData;
        grid.innerHTML = spaces.map(space => this.createSpaceCard(space)).join('');
    },

    createSpaceCard(space) {
        const statusClass = space.status === 'available' ? 'badge-available' : 'badge-occupied';
        const statusText = space.status === 'available' ? 'Disponível' : 'Ocupado';
        
        return `
            <div class="card" onclick="app.showSpaceDetail(${space.id})">
                <img src="${space.image}" alt="${space.name}" class="card-image">
                <div class="card-content">
                    <span class="card-badge ${statusClass}">${statusText}</span>
                    <h3 class="card-title">${space.name}</h3>
                    <p class="card-description">${space.description.substring(0, 100)}...</p>
                    <div class="card-meta">
                        <div class="card-meta-item">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                                <circle cx="9" cy="7" r="4"></circle>
                                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                            </svg>
                            ${space.capacity} pessoas
                        </div>
                        <div class="card-meta-item">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                            </svg>
                            ${space.floor}
                        </div>
                    </div>
                    <div class="card-footer" onclick="event.stopPropagation()">
                        <button class="btn-outline" onclick="app.showSpaceDetail(${space.id})">Ver Detalhes</button>
                        <button class="btn-primary" onclick="app.showBookingModal(${space.id}, 'space')" ${space.status === 'occupied' ? 'disabled' : ''}>
                            Reservar
                        </button>
                    </div>
                </div>
            </div>
        `;
    },

    showSpaceDetail(spaceId) {
        const space = spacesData.find(s => s.id === spaceId);
        if (!space) return;

        const content = `
            <div class="detail-header">
                <img src="${space.image}" alt="${space.name}" class="detail-image">
                <div class="detail-title">
                    <h2>${space.name}</h2>
                    <span class="card-badge ${space.status === 'available' ? 'badge-available' : 'badge-occupied'}">
                        ${space.status === 'available' ? 'Disponível' : 'Ocupado'}
                    </span>
                </div>
                <div class="detail-meta">
                    <div class="detail-meta-item">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                            <circle cx="9" cy="7" r="4"></circle>
                            <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                        </svg>
                        Capacidade: ${space.capacity} pessoas
                    </div>
                    <div class="detail-meta-item">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                        </svg>
                        ${space.floor}
                    </div>
                    <div class="detail-meta-item">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                        </svg>
                        Área: ${space.area}
                    </div>
                    <div class="detail-meta-item">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="3" y="3" width="7" height="7"></rect>
                            <rect x="14" y="3" width="7" height="7"></rect>
                            <rect x="14" y="14" width="7" height="7"></rect>
                            <rect x="3" y="14" width="7" height="7"></rect>
                        </svg>
                        Tipo: ${space.type}
                    </div>
                </div>
            </div>
            <div class="detail-section">
                <h3>Sobre o Ambiente</h3>
                <p>${space.description}</p>
            </div>
            <div class="detail-section">
                <h3>Recursos Disponíveis</h3>
                <ul class="detail-list">
                    ${space.features.map(feature => `
                        <li>
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <polyline points="20 6 9 17 4 12"></polyline>
                            </svg>
                            ${feature}
                        </li>
                    `).join('')}
                </ul>
            </div>
            <div class="detail-actions">
                <button class="btn-primary btn-full" onclick="app.showBookingModal(${spaceId}, 'space'); app.hideDetailModal()" ${space.status === 'occupied' ? 'disabled' : ''}>
                    Reservar Ambiente
                </button>
            </div>
        `;

        document.getElementById('detail-content').innerHTML = content;
        document.getElementById('detail-modal').classList.add('show');
    },

    // Render Equipment
    renderEquipment(gridId, limit = null) {
        const grid = document.getElementById(gridId);
        const equipment = limit ? equipmentData.slice(0, limit) : equipmentData;
        grid.innerHTML = equipment.map(item => this.createEquipmentCard(item)).join('');
    },

    createEquipmentCard(equipment) {
        const statusClass = equipment.status === 'available' ? 'badge-available' : 'badge-occupied';
        const statusText = equipment.status === 'available' ? 'Disponível' : 'Em uso';
        
        return `
            <div class="card" onclick="app.showEquipmentDetail(${equipment.id})">
                <img src="${equipment.image}" alt="${equipment.name}" class="card-image">
                <div class="card-content">
                    <span class="card-badge ${statusClass}">${statusText}</span>
                    <h3 class="card-title">${equipment.name}</h3>
                    <p class="card-description">${equipment.description.substring(0, 100)}...</p>
                    <div class="card-meta">
                        <div class="card-meta-item">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M20 7h-9"></path>
                                <path d="M14 17H5"></path>
                                <circle cx="17" cy="17" r="3"></circle>
                                <circle cx="7" cy="7" r="3"></circle>
                            </svg>
                            ${equipment.category}
                        </div>
                        <div class="card-meta-item">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
                            </svg>
                            ${equipment.condition}
                        </div>
                    </div>
                    <div class="card-footer" onclick="event.stopPropagation()">
                        <button class="btn-outline" onclick="app.showEquipmentDetail(${equipment.id})">Ver Detalhes</button>
                        <button class="btn-primary" onclick="app.showBookingModal(${equipment.id}, 'equipment')" ${equipment.status === 'occupied' ? 'disabled' : ''}>
                            Reservar
                        </button>
                    </div>
                </div>
            </div>
        `;
    },

    showEquipmentDetail(equipmentId) {
        const equipment = equipmentData.find(e => e.id === equipmentId);
        if (!equipment) return;

        const content = `
            <div class="detail-header">
                <img src="${equipment.image}" alt="${equipment.name}" class="detail-image">
                <div class="detail-title">
                    <h2>${equipment.name}</h2>
                    <span class="card-badge ${equipment.status === 'available' ? 'badge-available' : 'badge-occupied'}">
                        ${equipment.status === 'available' ? 'Disponível' : 'Em uso'}
                    </span>
                </div>
                <div class="detail-meta">
                    <div class="detail-meta-item">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M20 7h-9"></path>
                            <path d="M14 17H5"></path>
                            <circle cx="17" cy="17" r="3"></circle>
                            <circle cx="7" cy="7" r="3"></circle>
                        </svg>
                        ${equipment.category}
                    </div>
                    <div class="detail-meta-item">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
                            <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
                        </svg>
                        ${equipment.brand}
                    </div>
                    <div class="detail-meta-item">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
                        </svg>
                        Estado: ${equipment.condition}
                    </div>
                    <div class="detail-meta-item">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                            <polyline points="14 2 14 8 20 8"></polyline>
                        </svg>
                        Modelo: ${equipment.model}
                    </div>
                </div>
            </div>
            <div class="detail-section">
                <h3>Sobre o Equipamento</h3>
                <p>${equipment.description}</p>
            </div>
            <div class="detail-section">
                <h3>Especificações Técnicas</h3>
                <ul class="detail-list">
                    ${equipment.specifications.map(spec => `
                        <li>
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <polyline points="20 6 9 17 4 12"></polyline>
                            </svg>
                            ${spec}
                        </li>
                    `).join('')}
                </ul>
            </div>
            <div class="detail-actions">
                <button class="btn-primary btn-full" onclick="app.showBookingModal(${equipmentId}, 'equipment'); app.hideDetailModal()" ${equipment.status === 'occupied' ? 'disabled' : ''}>
                    Reservar Equipamento
                </button>
            </div>
        `;

        document.getElementById('detail-content').innerHTML = content;
        document.getElementById('detail-modal').classList.add('show');
    },

    // Render History
    renderHistory() {
        const list = document.getElementById('history-list');
        list.innerHTML = historyData.map(item => this.createHistoryItem(item)).join('');
    },

    createHistoryItem(item) {
        const iconClass = item.type === 'space' ? 'history-icon-purple' : 'history-icon-teal';
        const icon = item.type === 'space' 
            ? '<rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect>'
            : '<rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>';
        
        return `
            <div class="history-item">
                <div class="history-icon ${iconClass}">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        ${icon}
                    </svg>
                </div>
                <div class="history-content">
                    <div class="history-header">
                        <h4 class="history-title">${item.name}</h4>
                        <span class="history-date">${this.formatDate(item.date)}</span>
                    </div>
                    <p class="history-description">${item.purpose}</p>
                    <div class="history-meta">
                        <span>
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <circle cx="12" cy="12" r="10"></circle>
                                <polyline points="12 6 12 12 16 14"></polyline>
                            </svg>
                            ${item.startTime} - ${item.endTime}
                        </span>
                        <span class="card-badge badge-available">Concluído</span>
                    </div>
                </div>
            </div>
        `;
    },

    // Calendar
    renderCalendar() {
        const year = this.currentMonth.getFullYear();
        const month = this.currentMonth.getMonth();
        
        // Update month label
        const monthNames = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];
        document.getElementById('calendar-month').textContent = `${monthNames[month]} ${year}`;
        
        // Get first day of month and number of days
        const firstDay = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        
        // Generate calendar grid
        let html = '';
        
        // Day headers
        const dayHeaders = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];
        dayHeaders.forEach(day => {
            html += `<div class="calendar-day-header">${day}</div>`;
        });
        
        // Empty cells before first day
        for (let i = 0; i < firstDay; i++) {
            html += '<div class="calendar-day other-month"></div>';
        }
        
        // Days of month
        const today = new Date();
        for (let day = 1; day <= daysInMonth; day++) {
            const date = new Date(year, month, day);
            const dateStr = this.formatDateForComparison(date);
            const isToday = date.toDateString() === today.toDateString();
            const hasEvent = calendarEvents.some(e => e.date === dateStr);
            
            let classes = 'calendar-day';
            if (isToday) classes += ' today';
            if (hasEvent) classes += ' has-event';
            
            html += `<div class="${classes}">${day}</div>`;
        }
        
        document.getElementById('calendar-grid').innerHTML = html;
    },

    previousMonth() {
        this.currentMonth = new Date(this.currentMonth.getFullYear(), this.currentMonth.getMonth() - 1);
        this.renderCalendar();
    },

    nextMonth() {
        this.currentMonth = new Date(this.currentMonth.getFullYear(), this.currentMonth.getMonth() + 1);
        this.renderCalendar();
    },

    renderUpcomingEvents() {
        const list = document.getElementById('upcoming-events-list');
        const upcoming = calendarEvents.slice(0, 3);
        
        list.innerHTML = upcoming.map(event => `
            <div class="upcoming-event">
                <div class="upcoming-event-title">${event.title}</div>
                <div class="upcoming-event-time">${this.formatDate(event.date)} • ${event.time}</div>
            </div>
        `).join('');
    },

    // Booking
    showBookingModal(itemId, type) {
        this.currentBookingItem = itemId;
        this.currentBookingType = type;
        
        const item = type === 'space' 
            ? spacesData.find(s => s.id === itemId)
            : equipmentData.find(e => e.id === itemId);
        
        document.getElementById('booking-item-name').textContent = item.name;
        
        // Set minimum date to today
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('booking-date').setAttribute('min', today);
        
        document.getElementById('booking-modal').classList.add('show');
    },

    hideBookingModal() {
        document.getElementById('booking-modal').classList.remove('show');
        document.getElementById('booking-form').reset();
    },

    handleBooking(event) {
        event.preventDefault();
        
        const date = document.getElementById('booking-date').value;
        const startTime = document.getElementById('booking-start').value;
        const endTime = document.getElementById('booking-end').value;
        const purpose = document.getElementById('booking-purpose').value;
        
        // Validate times
        if (startTime >= endTime) {
            alert('O horário de início deve ser anterior ao horário de fim.');
            return;
        }
        
        // Simulate booking
        alert('Agendamento realizado com sucesso!');
        this.hideBookingModal();
        
        // Add to history (in a real app, this would be saved to database)
        const item = this.currentBookingType === 'space'
            ? spacesData.find(s => s.id === this.currentBookingItem)
            : equipmentData.find(e => e.id === this.currentBookingItem);
        
        historyData.unshift({
            id: Date.now(),
            type: this.currentBookingType,
            name: item.name,
            date: date,
            startTime: startTime,
            endTime: endTime,
            purpose: purpose,
            status: 'pending'
        });
        
        this.renderHistory();
    },

    hideDetailModal() {
        document.getElementById('detail-modal').classList.remove('show');
    },

    // Utilities
    formatDate(dateStr) {
        const date = new Date(dateStr + 'T00:00:00');
        return date.toLocaleDateString('pt-BR', { day: '2-digit', month: 'short', year: 'numeric' });
    },

    formatDateForComparison(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    },

    setupFormValidation() {
        // Add real-time validation to forms if needed
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                if (!form.checkValidity()) {
                    e.preventDefault();
                    e.stopPropagation();
                }
            });
        });
    },

    // Admin Functions
    renderUsers() {
        const tbody = document.getElementById('users-table-body');
        tbody.innerHTML = usersData.map(user => `
            <tr>
                <td>${user.name}</td>
                <td>${user.email}</td>
                <td>${this.getRoleLabel(user.role)}</td>
                <td><span class="user-status ${user.status}">${user.status === 'active' ? 'Ativo' : 'Inativo'}</span></td>
                <td>
                    <div class="table-actions">
                        <button class="table-action-btn table-action-edit" onclick="app.editUser(${user.id})">Editar</button>
                        <button class="table-action-btn table-action-delete" onclick="app.deleteUser(${user.id})">Excluir</button>
                    </div>
                </td>
            </tr>
        `).join('');
    },

    getRoleLabel(role) {
        const roles = {
            'admin': 'Administrador',
            'user': 'Usuário',
            'moderator': 'Moderador'
        };
        return roles[role] || role;
    },

    showAddUserModal() {
        document.getElementById('add-user-modal').classList.add('show');
    },

    hideAddUserModal() {
        document.getElementById('add-user-modal').classList.remove('show');
        document.getElementById('add-user-form').reset();
    },

    handleAddUser(event) {
        event.preventDefault();
        
        const name = document.getElementById('user-name').value;
        const email = document.getElementById('user-email').value;
        const role = document.getElementById('user-role').value;
        const status = document.getElementById('user-status').value;
        
        const newUser = {
            id: usersData.length + 1,
            name,
            email,
            role,
            status
        };
        
        usersData.push(newUser);
        this.renderUsers();
        this.hideAddUserModal();
        alert('Usuário adicionado com sucesso!');
    },

    editUser(userId) {
        const user = usersData.find(u => u.id === userId);
        if (!user) return;
        
        const newName = prompt('Nome:', user.name);
        if (newName && newName !== user.name) {
            user.name = newName;
            this.renderUsers();
        }
    },

    deleteUser(userId) {
        if (confirm('Deseja realmente excluir este usuário?')) {
            const index = usersData.findIndex(u => u.id === userId);
            if (index !== -1) {
                usersData.splice(index, 1);
                this.renderUsers();
                alert('Usuário excluído com sucesso!');
            }
        }
    },

    renderPendingBookings() {
        const list = document.getElementById('pending-bookings-list');
        
        if (pendingBookingsData.length === 0) {
            list.innerHTML = '<p style="text-align: center; color: var(--gray-600); padding: 2rem;">Nenhum agendamento pendente</p>';
            return;
        }
        
        list.innerHTML = pendingBookingsData.map(booking => `
            <div class="pending-booking-card">
                <div class="pending-booking-info">
                    <div class="pending-booking-header">
                        <h4 class="pending-booking-title">${booking.itemName}</h4>
                        <span class="card-badge badge-purple">${booking.type === 'space' ? 'Ambiente' : 'Equipamento'}</span>
                    </div>
                    <div class="pending-booking-meta">
                        <span>
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                                <circle cx="9" cy="7" r="4"></circle>
                            </svg>
                            ${booking.userName}
                        </span>
                        <span>
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                                <line x1="16" y1="2" x2="16" y2="6"></line>
                                <line x1="8" y1="2" x2="8" y2="6"></line>
                                <line x1="3" y1="10" x2="21" y2="10"></line>
                            </svg>
                            ${this.formatDate(booking.date)}
                        </span>
                        <span>
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <circle cx="12" cy="12" r="10"></circle>
                                <polyline points="12 6 12 12 16 14"></polyline>
                            </svg>
                            ${booking.startTime} - ${booking.endTime}
                        </span>
                    </div>
                    <p class="pending-booking-description">${booking.purpose}</p>
                </div>
                <div class="pending-booking-actions">
                    <button class="btn-approve" onclick="app.approveBooking(${booking.id})">Aprovar</button>
                    <button class="btn-reject" onclick="app.rejectBooking(${booking.id})">Rejeitar</button>
                </div>
            </div>
        `).join('');
    },

    approveBooking(bookingId) {
        if (confirm('Aprovar este agendamento?')) {
            const index = pendingBookingsData.findIndex(b => b.id === bookingId);
            if (index !== -1) {
                pendingBookingsData.splice(index, 1);
                this.renderPendingBookings();
                alert('Agendamento aprovado com sucesso!');
            }
        }
    },

    rejectBooking(bookingId) {
        if (confirm('Rejeitar este agendamento?')) {
            const index = pendingBookingsData.findIndex(b => b.id === bookingId);
            if (index !== -1) {
                pendingBookingsData.splice(index, 1);
                this.renderPendingBookings();
                alert('Agendamento rejeitado.');
            }
        }
    },

    toggleSetting(settingName, value) {
        systemSettings[settingName] = value;
        console.log(`Setting ${settingName} changed to:`, value);
        alert(`Configuração atualizada!`);
    },

    updateSetting(settingName, value) {
        systemSettings[settingName] = parseInt(value);
        console.log(`Setting ${settingName} changed to:`, value);
    }
};

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        // App will be initialized after login
    });
} else {
    // DOM is already ready
}