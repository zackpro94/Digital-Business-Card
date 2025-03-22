// Main JavaScript file for Digital Business Card

document.addEventListener('DOMContentLoaded', function() {
    // Initialize AOS animation library
    AOS.init({
        duration: 800,
        easing: 'ease-in-out',
        once: false,
        mirror: false
    });

    // Initialize all tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize all popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card, .business-card, .feature-card, .dashboard-card');
    cards.forEach((card, index) => {
        card.classList.add('fade-in');
        card.style.animationDelay = `${index * 0.1}s`;
    });

    // Add floating animation to specific elements
    addFloatingAnimation();

    // Save Contact function
    window.saveContact = function() {
        // Create vCard data
        let vCardData = createVCardData();
        
        // Create downloadable link
        const blob = new Blob([vCardData], { type: 'text/vcard' });
        const url = URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = 'contact.vcf';
        link.click();
        
        // Clean up
        URL.revokeObjectURL(url);
        
        // Show success message
        const toast = new bootstrap.Toast(document.getElementById('contactSavedToast'));
        toast.show();
    }

    // Create vCard data from page
    function createVCardData() {
        const name = document.querySelector('.business-card h1') ? 
                     document.querySelector('.business-card h1').textContent.trim() : '';
        
        const jobTitle = document.querySelector('.business-card .text-muted') ? 
                         document.querySelector('.business-card .text-muted').textContent.trim() : '';
        
        const companyName = document.querySelector('.company-name') ? 
                           document.querySelector('.company-name').textContent.trim() : '';
        
        let phone = '';
        let email = '';
        let website = '';
        
        const contactInfo = document.querySelectorAll('.contact-info a');
        contactInfo.forEach(info => {
            if (info.href.startsWith('tel:')) {
                phone = info.textContent.trim();
            } else if (info.href.startsWith('mailto:')) {
                email = info.textContent.trim();
            } else if (info.href.startsWith('http')) {
                website = info.textContent.trim();
            }
        });
        
        // Create vCard format
        return `BEGIN:VCARD
VERSION:3.0
N:${name}
FN:${name}
TITLE:${jobTitle}
ORG:${companyName}
TEL;TYPE=WORK,VOICE:${phone}
EMAIL;TYPE=WORK:${email}
URL:${website}
END:VCARD`;
    }

    // Share functionality
    const shareButtons = document.querySelectorAll('.share-btn');
    if (shareButtons.length > 0) {
        shareButtons.forEach(btn => {
            btn.addEventListener('click', function(e) {
                if (navigator.share) {
                    navigator.share({
                        title: document.title,
                        text: 'Check out my digital business card!',
                        url: window.location.href
                    })
                    .then(() => console.log('Share successful'))
                    .catch((error) => console.log('Error sharing', error));
                    
                    e.preventDefault();
                }
            });
        });
    }

    // Analytics chart initialization
    const analyticsCharts = document.querySelectorAll('.analytics-chart');
    if (analyticsCharts.length > 0) {
        initializeCharts();
    }

    function initializeCharts() {
        // This function would initialize charts using a library like Chart.js
        console.log('Analytics charts initialized');
    }

    // Dark mode toggle
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            
            // Save preference to localStorage
            const isDarkMode = document.body.classList.contains('dark-mode');
            localStorage.setItem('darkMode', isDarkMode);
            
            // Update icon
            const icon = this.querySelector('i');
            if (isDarkMode) {
                icon.classList.remove('fa-moon');
                icon.classList.add('fa-sun');
            } else {
                icon.classList.remove('fa-sun');
                icon.classList.add('fa-moon');
            }
        });
        
        // Check for saved preference
        const savedDarkMode = localStorage.getItem('darkMode');
        if (savedDarkMode === 'true') {
            document.body.classList.add('dark-mode');
            const icon = darkModeToggle.querySelector('i');
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        }
    }
});

// Add floating animation to specific elements
function addFloatingAnimation() {
    const elements = document.querySelectorAll('.floating-element');
    elements.forEach(element => {
        // Apply the animation directly from JavaScript to ensure it works
        element.style.animation = 'float 6s ease-in-out infinite';
    });
}

// Function to handle card sharing
function shareCard(uuid) {
    const shareUrl = `${window.location.origin}/card/${uuid}/share/`;
    
    // Set the X-Requested-With header to indicate an AJAX request
    fetch(shareUrl, { 
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Update share count in UI without page reload
            const shareCountElement = document.querySelector('.share-count');
            if (shareCountElement) {
                shareCountElement.textContent = data.shares;
            }
            
            // Show success toast
            const shareToast = document.getElementById('shareToast') || document.getElementById('contactSavedToast') || document.getElementById('dashboardToast');
            if (shareToast) {
                const toastBody = shareToast.querySelector('.toast-body');
                if (toastBody) {
                    toastBody.textContent = 'Card shared successfully!';
                }
                const toastHeader = shareToast.querySelector('.toast-header strong');
                if (toastHeader) {
                    toastHeader.textContent = 'Shared';
                }
                
                const toastInstance = new bootstrap.Toast(shareToast, {
                    autohide: true,
                    delay: 3000
                });
                toastInstance.show();
            }
        }
    })
    .catch(error => {
        console.error('Error sharing card:', error);
    });
    
    // Try to use the Web Share API if available
    if (navigator.share) {
        const cardUrl = `${window.location.origin}/card/${uuid}/`;
        navigator.share({
            title: document.title || 'Digital Business Card',
            text: 'Check out this digital business card!',
            url: cardUrl
        })
        .then(() => console.log('Successfully shared'))
        .catch((error) => console.log('Error sharing:', error));
    }
}

// Make shareCard available globally
window.shareCard = shareCard;

// Function to copy a card link to clipboard
function copyCardLink(url) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(url)
            .then(function() {
                // Show success toast
                const toast = document.getElementById('copyToast') || document.getElementById('contactSavedToast') || document.getElementById('dashboardToast');
                if (toast) {
                    const toastBody = toast.querySelector('.toast-body');
                    if (toastBody) {
                        toastBody.textContent = 'Link copied to clipboard!';
                    }
                    const toastHeader = toast.querySelector('.toast-header strong');
                    if (toastHeader) {
                        toastHeader.textContent = 'Success';
                    }
                    
                    const toastInstance = new bootstrap.Toast(toast, {
                        autohide: true,
                        delay: 3000
                    });
                    toastInstance.show();
                }
            })
            .catch(function(err) {
                console.error('Failed to copy link: ', err);
                alert('Failed to copy link to clipboard');
            });
    } else {
        // Fallback for browsers that don't support clipboard API
        try {
            const tempInput = document.createElement('input');
            document.body.appendChild(tempInput);
            tempInput.value = url;
            tempInput.select();
            document.execCommand('copy');
            document.body.removeChild(tempInput);
            
            // Show success toast
            const toast = document.getElementById('copyToast') || document.getElementById('contactSavedToast') || document.getElementById('dashboardToast');
            if (toast) {
                const toastBody = toast.querySelector('.toast-body');
                if (toastBody) {
                    toastBody.textContent = 'Link copied to clipboard!';
                }
                const toastHeader = toast.querySelector('.toast-header strong');
                if (toastHeader) {
                    toastHeader.textContent = 'Success';
                }
                
                const toastInstance = new bootstrap.Toast(toast, {
                    autohide: true,
                    delay: 3000
                });
                toastInstance.show();
            }
        } catch (err) {
            console.error('Failed to copy link: ', err);
            alert('Failed to copy link to clipboard');
        }
    }
}

// Make copyCardLink available globally
window.copyCardLink = copyCardLink;

// QR Code animation on hover
document.addEventListener('DOMContentLoaded', function() {
    const qrCodeContainer = document.querySelector('.qr-code-container');
    if (qrCodeContainer) {
        qrCodeContainer.addEventListener('mouseenter', () => {
            qrCodeContainer.classList.add('qr-hover');
        });
        
        qrCodeContainer.addEventListener('mouseleave', () => {
            qrCodeContainer.classList.remove('qr-hover');
        });
    }
});
