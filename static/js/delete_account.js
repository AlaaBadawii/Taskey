function confirmDelete(event) {
    event.preventDefault();
    console.log("confirmDelete() function is called.");
    if (confirm("Are you sure you want to delete your account?")) {
        document.getElementById('delete-user-form').submit();
    }
}
