// Handle category selection change
document.getElementById('category-select').addEventListener('change', function() {
    this.form.submit();
});

// Or if you want to keep them separate but sync them:
document.querySelector('.search-category-form').addEventListener('submit', function(e) {
    // You can add any pre-submit logic here if needed
});