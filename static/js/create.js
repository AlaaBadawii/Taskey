document.addEventListener('DOMContentLoaded', () => {
    const autoGrowTextareas = document.querySelectorAll('textarea[data-auto-grow]');
    autoGrowTextareas.forEach((textarea) => {
        const resizeTextarea = () => {
            textarea.style.height = 'auto';
            textarea.style.height = `${textarea.scrollHeight}px`;
        };

        textarea.addEventListener('input', resizeTextarea);
        resizeTextarea();
    });

    const stepsBuilder = document.querySelector('[data-steps-builder]');
    if (stepsBuilder) {
        const stepsList = stepsBuilder.querySelector('[data-steps-list]');
        const addStepButton = stepsBuilder.querySelector('[data-add-step]');
        const stepTemplate = document.getElementById('task-step-template');

        const updateStepLabels = () => {
            const stepItems = stepsList.querySelectorAll('.task-step-item');
            stepItems.forEach((stepItem, index) => {
                const badge = stepItem.querySelector('.step-badge');
                if (badge) {
                    badge.textContent = `Step ${index + 1}`;
                }
            });
        };

        const attachStepEvents = (stepItem) => {
            const stepInput = stepItem.querySelector('input[name="task_steps[]"]');
            const removeButton = stepItem.querySelector('[data-remove-step]');

            if (removeButton) {
                removeButton.addEventListener('click', () => {
                    stepItem.remove();
                    updateStepLabels();
                });
            }

            if (stepInput) {
                stepInput.addEventListener('keydown', (event) => {
                    if (event.key === 'Enter') {
                        event.preventDefault();
                        addStep();
                    }
                });
            }
        };

        const addStep = (value = '') => {
            const stepFragment = stepTemplate.content.cloneNode(true);
            const stepItem = stepFragment.querySelector('.task-step-item');
            const stepInput = stepFragment.querySelector('input[name="task_steps[]"]');

            stepInput.value = value;
            stepsList.appendChild(stepItem);
            attachStepEvents(stepItem);
            updateStepLabels();
            stepInput.focus();
        };

        stepsList.querySelectorAll('.task-step-item').forEach((stepItem) => {
            attachStepEvents(stepItem);
        });
        updateStepLabels();

        addStepButton.addEventListener('click', () => addStep());
    }

    const picker = document.querySelector('[data-date-picker]');
    if (!picker) {
        return;
    }

    const hiddenInput = picker.querySelector('#due_date');
    const toggle = picker.querySelector('[data-date-toggle]');
    const panel = picker.querySelector('[data-date-panel]');
    const monthLabel = picker.querySelector('[data-date-month]');
    const grid = picker.querySelector('[data-date-grid]');
    const valueLabel = picker.querySelector('[data-date-value]');
    const prevButton = picker.querySelector('[data-date-prev]');
    const nextButton = picker.querySelector('[data-date-next]');
    const todayButton = picker.querySelector('[data-date-today]');
    const clearButton = picker.querySelector('[data-date-clear]');

    const today = new Date();
    const todayAtMidnight = new Date(today.getFullYear(), today.getMonth(), today.getDate());

    let selectedDate = null;
    let visibleMonth = new Date(todayAtMidnight.getFullYear(), todayAtMidnight.getMonth(), 1);

    function formatDisplayDate(date) {
        return new Intl.DateTimeFormat('en-US', {
            weekday: 'short',
            month: 'short',
            day: 'numeric',
            year: 'numeric'
        }).format(date);
    }

    function formatMonth(date) {
        return new Intl.DateTimeFormat('en-US', {
            month: 'long',
            year: 'numeric'
        }).format(date);
    }

    function formatIsoDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    function parseIsoDate(value) {
        if (!value) {
            return null;
        }

        const parts = value.split('-').map(Number);
        if (parts.length !== 3 || parts.some(Number.isNaN)) {
            return null;
        }

        return new Date(parts[0], parts[1] - 1, parts[2]);
    }

    function sameDay(a, b) {
        return a &&
            b &&
            a.getFullYear() === b.getFullYear() &&
            a.getMonth() === b.getMonth() &&
            a.getDate() === b.getDate();
    }

    function updateDisplay() {
        if (selectedDate) {
            valueLabel.textContent = formatDisplayDate(selectedDate);
        } else {
            valueLabel.textContent = 'Select when this task should be done';
        }
    }

    function setSelectedDate(date) {
        selectedDate = date ? new Date(date.getFullYear(), date.getMonth(), date.getDate()) : null;
        hiddenInput.value = selectedDate ? formatIsoDate(selectedDate) : '';
        if (selectedDate) {
            picker.classList.remove('is-invalid');
        }
        updateDisplay();
        renderCalendar();
    }

    function openPanel() {
        panel.hidden = false;
        toggle.setAttribute('aria-expanded', 'true');
    }

    function closePanel() {
        panel.hidden = true;
        toggle.setAttribute('aria-expanded', 'false');
    }

    function renderCalendar() {
        monthLabel.textContent = formatMonth(visibleMonth);
        grid.innerHTML = '';

        const firstDay = new Date(visibleMonth.getFullYear(), visibleMonth.getMonth(), 1);
        const startDay = firstDay.getDay();
        const daysInMonth = new Date(visibleMonth.getFullYear(), visibleMonth.getMonth() + 1, 0).getDate();
        const daysInPrevMonth = new Date(visibleMonth.getFullYear(), visibleMonth.getMonth(), 0).getDate();

        for (let index = 0; index < 42; index += 1) {
            const cell = document.createElement('button');
            cell.type = 'button';
            cell.className = 'date-cell';

            let date;
            if (index < startDay) {
                const day = daysInPrevMonth - startDay + index + 1;
                date = new Date(visibleMonth.getFullYear(), visibleMonth.getMonth() - 1, day);
                cell.classList.add('is-muted');
            } else if (index >= startDay + daysInMonth) {
                const day = index - (startDay + daysInMonth) + 1;
                date = new Date(visibleMonth.getFullYear(), visibleMonth.getMonth() + 1, day);
                cell.classList.add('is-muted');
            } else {
                const day = index - startDay + 1;
                date = new Date(visibleMonth.getFullYear(), visibleMonth.getMonth(), day);
            }

            cell.textContent = String(date.getDate());
            cell.dataset.date = formatIsoDate(date);
            cell.setAttribute('aria-label', formatDisplayDate(date));

            if (sameDay(date, todayAtMidnight)) {
                cell.classList.add('is-today');
            }

            if (sameDay(date, selectedDate)) {
                cell.classList.add('is-selected');
            }

            cell.addEventListener('click', () => {
                visibleMonth = new Date(date.getFullYear(), date.getMonth(), 1);
                setSelectedDate(date);
                closePanel();
            });

            grid.appendChild(cell);
        }
    }

    toggle.addEventListener('click', () => {
        if (panel.hidden) {
            openPanel();
        } else {
            closePanel();
        }
    });

    prevButton.addEventListener('click', () => {
        visibleMonth = new Date(visibleMonth.getFullYear(), visibleMonth.getMonth() - 1, 1);
        renderCalendar();
    });

    nextButton.addEventListener('click', () => {
        visibleMonth = new Date(visibleMonth.getFullYear(), visibleMonth.getMonth() + 1, 1);
        renderCalendar();
    });

    todayButton.addEventListener('click', () => {
        visibleMonth = new Date(todayAtMidnight.getFullYear(), todayAtMidnight.getMonth(), 1);
        setSelectedDate(todayAtMidnight);
        closePanel();
    });

    clearButton.addEventListener('click', () => {
        setSelectedDate(null);
    });

    picker.closest('form').addEventListener('submit', (event) => {
        if (!hiddenInput.value) {
            event.preventDefault();
            picker.classList.add('is-invalid');
            openPanel();
            toggle.focus();
            valueLabel.textContent = 'Please choose a due date before creating the task';
        }
    });

    document.addEventListener('click', (event) => {
        if (!picker.contains(event.target)) {
            closePanel();
        }
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            closePanel();
        }
    });

    const initialDate = parseIsoDate(hiddenInput.value);
    if (initialDate) {
        visibleMonth = new Date(initialDate.getFullYear(), initialDate.getMonth(), 1);
        setSelectedDate(initialDate);
    }

    updateDisplay();
    renderCalendar();
});
