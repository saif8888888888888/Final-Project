// Initialize charts
function initCharts(resultData, platformData) {
    // Results chart
    const resultsCtx = document.getElementById('resultsChart');
    if (resultsCtx) {
        const resultsChart = new Chart(resultsCtx, {
            type: 'doughnut',
            data: resultData,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#e0e0ff',
                            font: {
                                size: 12
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Platforms chart
    const platformsCtx = document.getElementById('platformsChart');
    if (platformsCtx) {
        const platformsChart = new Chart(platformsCtx, {
            type: 'bar',
            data: {
                labels: platformData.labels,
                datasets: [{
                    label: '# of Scans',
                    data: platformData.datasets[0].data,
                    backgroundColor: platformData.datasets[0].backgroundColor,
                    borderColor: platformData.datasets[0].backgroundColor.map(color => 
                        color.replace('0.8', '1')
                    ),
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: '#e0e0ff',
                            font: {
                                size: 12
                            }
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    },
                    x: {
                        ticks: {
                            color: '#e0e0ff',
                            font: {
                                size: 12
                            }
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
}

// Load scan history
function loadScanHistory() {
    // This would typically make an API call to fetch scan history
    console.log('Loading scan history...');
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Sidebar menu functionality
    const sidebarItems = document.querySelectorAll('.sidebar-menu li');
    sidebarItems.forEach(item => {
        item.addEventListener('click', function() {
            sidebarItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // User dropdown functionality
    const userDropdown = document.querySelector('.user-dropdown');
    if (userDropdown) {
        userDropdown.addEventListener('click', function(e) {
            const dropdownContent = this.querySelector('.dropdown-content');
            const isVisible = dropdownContent.style.display === 'block';
            dropdownContent.style.display = isVisible ? 'none' : 'block';
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!userDropdown.contains(e.target)) {
                const dropdownContent = userDropdown.querySelector('.dropdown-content');
                dropdownContent.style.display = 'none';
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