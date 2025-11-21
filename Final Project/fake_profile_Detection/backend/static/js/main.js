document.addEventListener('DOMContentLoaded', function() {
    // Platform selection
    const platformIcons = document.querySelectorAll('.platform-icon');
    const platformInput = document.getElementById('platform');
    
    if (platformIcons.length > 0 && platformInput) {
        platformIcons.forEach(icon => {
            icon.addEventListener('click', function() {
                platformIcons.forEach(i => i.classList.remove('active'));
                this.classList.add('active');
                
                // Update platform value
                const platform = this.getAttribute('data-platform');
                platformInput.value = platform;
                
                // Update placeholder based on platform
                const urlInput = document.getElementById('profile-url');
                
                switch(platform) {
                    case 'facebook':
                        urlInput.placeholder = 'https://www.facebook.com/username';
                        break;
                    case 'twitter':
                        urlInput.placeholder = 'https://www.twitter.com/username';
                        break;
                    case 'instagram':
                        urlInput.placeholder = 'https://www.instagram.com/username';
                        break;
                    case 'tiktok':
                        urlInput.placeholder = 'https://www.tiktok.com/@username';
                        break;
                }
            });
        });
    }
    
    // Form submission handling
    const form = document.getElementById('profile-check-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            // Show loading state
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
            submitBtn.disabled = true;
            
            // Re-enable after 3 seconds (for demo purposes)
            setTimeout(() => {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 3000);
        });
    }
    
    // User dropdown functionality
    const userDropdown = document.querySelector('.user-dropdown');
    if (userDropdown) {
        userDropdown.addEventListener('click', function(e) {
            const dropdownContent = this.querySelector('.dropdown-content');
            dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!userDropdown.contains(e.target)) {
                const dropdownContent = userDropdown.querySelector('.dropdown-content');
                dropdownContent.style.display = 'none';
            }
        });
    }
    
    // Logout functionality
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            if (confirm('Are you sure you want to logout?')) {
                window.location.href = this.href;
            }
        });
    }
    
    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.alert');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });
});