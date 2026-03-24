// Get the current date
const currentDate = new Date();
// Get the day number
const dayNumber = currentDate.getDate();
// Update the text of the span element with the day number
const currentDateElement = document.getElementById('current-date');
if (currentDateElement) {
    currentDateElement.textContent = dayNumber;
}

document.addEventListener('DOMContentLoaded', (event) => {
    const menuToggle = document.getElementById('menu-toggle');
    const menu = document.getElementById('menu');
    const headerAccount = document.querySelector('.header-account');
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('sidebar-nav');
    const sidebarClose = document.getElementById('sidebar-close');
    const sidebarBackdrop = document.getElementById('sidebar-backdrop');

    if (menuToggle && menu && headerAccount) {
        const closeMenu = () => {
            menu.classList.remove('is-open');
            menuToggle.setAttribute('aria-expanded', 'false');
            menu.setAttribute('aria-hidden', 'true');
        };

        const openMenu = () => {
            menu.classList.add('is-open');
            menuToggle.setAttribute('aria-expanded', 'true');
            menu.setAttribute('aria-hidden', 'false');
        };

        menuToggle.addEventListener('click', () => {
            const isOpen = menu.classList.contains('is-open');
            if (isOpen) {
                closeMenu();
            } else {
                openMenu();
            }
        });

        document.addEventListener('click', (clickEvent) => {
            if (!headerAccount.contains(clickEvent.target)) {
                closeMenu();
            }
        });

        document.addEventListener('keydown', (keyEvent) => {
            if (keyEvent.key === 'Escape') {
                closeMenu();
            }
        });
    }

    if (sidebarToggle && sidebar && sidebarClose && sidebarBackdrop) {
        const closeSidebar = () => {
            sidebar.classList.remove('is-open');
            sidebarBackdrop.classList.remove('is-visible');
            sidebarToggle.setAttribute('aria-expanded', 'false');
            document.body.classList.remove('sidebar-open');
        };

        const openSidebar = () => {
            sidebar.classList.add('is-open');
            sidebarBackdrop.classList.add('is-visible');
            sidebarToggle.setAttribute('aria-expanded', 'true');
            document.body.classList.add('sidebar-open');
        };

        sidebarToggle.addEventListener('click', () => {
            const isOpen = sidebar.classList.contains('is-open');
            if (isOpen) {
                closeSidebar();
            } else {
                openSidebar();
            }
        });

        sidebarClose.addEventListener('click', closeSidebar);
        sidebarBackdrop.addEventListener('click', closeSidebar);

        document.addEventListener('keydown', (keyEvent) => {
            if (keyEvent.key === 'Escape') {
                closeSidebar();
            }
        });
    }

    const taskMenuButtons = document.querySelectorAll('[data-task-menu-toggle]');
    if (taskMenuButtons.length > 0) {
        const closeTaskMenu = (button) => {
            const taskCard = button.closest('.task');
            const menu = taskCard ? taskCard.querySelector('[data-task-menu]') : null;
            if (!menu) {
                return;
            }

            menu.classList.remove('is-open');
            button.setAttribute('aria-expanded', 'false');
        };

        const openTaskMenu = (button) => {
            const taskCard = button.closest('.task');
            const menu = taskCard ? taskCard.querySelector('[data-task-menu]') : null;
            if (!menu) {
                return;
            }

            menu.classList.add('is-open');
            button.setAttribute('aria-expanded', 'true');
        };

        const closeAllTaskMenus = (exceptButton = null) => {
            taskMenuButtons.forEach((button) => {
                if (button !== exceptButton) {
                    closeTaskMenu(button);
                }
            });
        };

        taskMenuButtons.forEach((button) => {
            button.addEventListener('click', (event) => {
                event.stopPropagation();
                const isExpanded = button.getAttribute('aria-expanded') === 'true';

                closeAllTaskMenus(button);

                if (isExpanded) {
                    closeTaskMenu(button);
                } else {
                    openTaskMenu(button);
                }
            });
        });

        document.addEventListener('click', (clickEvent) => {
            if (!clickEvent.target.closest('.task')) {
                closeAllTaskMenus();
            } else if (!clickEvent.target.closest('[data-task-menu]') && !clickEvent.target.closest('[data-task-menu-toggle]')) {
                closeAllTaskMenus();
            }
        });

        document.addEventListener('keydown', (keyEvent) => {
            if (keyEvent.key === 'Escape') {
                closeAllTaskMenus();
            }
        });
    }

    const groupsList = document.querySelector('.container nav ul.groups');
    if (groupsList) {
        const groupItems = Array.from(groupsList.querySelectorAll('li')).slice(1);
        const maxVisibleGroups = 3;

        if (groupItems.length > maxVisibleGroups) {
            const toggleItem = document.createElement('li');
            toggleItem.className = 'groups-toggle-item';

            const toggleButton = document.createElement('button');
            toggleButton.type = 'button';
            toggleButton.className = 'groups-toggle-btn';
            toggleButton.textContent = 'View more';
            toggleButton.setAttribute('aria-expanded', 'false');

            toggleItem.appendChild(toggleButton);
            groupsList.appendChild(toggleItem);

            const expandGroups = () => {
                groupsList.classList.add('is-expanded');
                toggleButton.textContent = 'Show less';
                toggleButton.setAttribute('aria-expanded', 'true');
            };

            const collapseGroups = () => {
                groupsList.classList.remove('is-expanded');
                toggleButton.textContent = 'View more';
                toggleButton.setAttribute('aria-expanded', 'false');
            };

            groupItems.forEach((item, index) => {
                if (index >= maxVisibleGroups) {
                    item.classList.add('group-item-extra');
                }
            });

            if (groupItems.some((item) => item.classList.contains('active') && item.classList.contains('group-item-extra'))) {
                expandGroups();
            }

            toggleButton.addEventListener('click', () => {
                const isExpanded = groupsList.classList.contains('is-expanded');
                if (isExpanded) {
                    collapseGroups();
                } else {
                    expandGroups();
                }
            });
        }
    }

    const video = document.getElementById('myVideo');
    if (!video) {
        return;
    }

    // Function to play video when in view and reset when out of view
    const handleIntersection = (entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                video.play().catch(error => {
                    console.log('Video play was prevented:', error);
                });
            } else {
                video.pause();
                video.currentTime = 0; // Reset the video to the beginning
            }
        });
    };

    // Create intersection observer
    const observer = new IntersectionObserver(handleIntersection, {
        threshold: 0.5 // Adjust this value as needed
    });

    // Start observing the video element
    observer.observe(video);
});
