/**
 * This function is used to confirm the deletion of a user account.
 * It prevents the default form submission and instead shows a confirmation dialog.
 * If the user confirms, the form is manually submitted.
 */
function confirmDelete(event) {
    // Prevent the default form submission
    event.preventDefault();

    // Log to the console that this function has been called
    console.log("confirmDelete() function is called.");

    // Show a confirmation dialog to the user
    // If the user confirms, submit the form
    if (confirm("Are you sure you want to delete your account?")) {
        document.getElementById('delete-user-form').submit();
    }
}