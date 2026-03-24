document.addEventListener('DOMContentLoaded', () => {
    const stepsForm = document.querySelector('[data-task-steps-form]');
    if (!stepsForm) {
        return;
    }

    const stepInputs = Array.from(stepsForm.querySelectorAll('.task-step-input'));
    const actions = stepsForm.querySelector('[data-step-actions]');
    const initialStates = stepInputs.map((input) => input.checked);
    let isSubmitting = false;

    const syncStepItem = (input) => {
        const stepItem = input.closest('[data-step-item]');
        if (!stepItem) {
            return;
        }

        stepItem.classList.toggle('is-completed', input.checked);
    };

    const hasUnsavedChanges = () => stepInputs.some((input, index) => input.checked !== initialStates[index]);

    const updateActions = () => {
        if (!actions) {
            return;
        }

        actions.hidden = !hasUnsavedChanges();
    };

    stepInputs.forEach((input) => {
        syncStepItem(input);
        input.addEventListener('change', () => {
            syncStepItem(input);
            updateActions();
        });
    });

    const confirmLeave = (event) => {
        if (isSubmitting || !hasUnsavedChanges()) {
            return;
        }

        event.preventDefault();
        event.returnValue = '';
    };

    window.addEventListener('beforeunload', confirmLeave);

    document.querySelectorAll('a[href]').forEach((link) => {
        if (stepsForm.contains(link)) {
            return;
        }

        link.addEventListener('click', (event) => {
            if (isSubmitting || !hasUnsavedChanges()) {
                return;
            }

            if (link.target === '_blank' || link.hasAttribute('download')) {
                return;
            }

            const shouldLeave = window.confirm('You have unsaved step changes. Leave this page without saving?');
            if (!shouldLeave) {
                event.preventDefault();
            }
        });
    });

    stepsForm.addEventListener('submit', () => {
        isSubmitting = true;
        window.removeEventListener('beforeunload', confirmLeave);
    });

    updateActions();
});
