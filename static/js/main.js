// Calcuingo - Main JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the app
    initializeApp();
    
    // Load user stats if logged in
    if (document.querySelector('#xp-counter')) {
        loadUserStats();
    }
    
    // Initialize lesson interactions
    initializeLessonInteractions();
    
    // Initialize mascot
    initializeMascot();
});

function initializeApp() {
    console.log('🧮 Calcuingo initialized!');
    
    // Add smooth scrolling
    document.documentElement.style.scrollBehavior = 'smooth';
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function loadUserStats() {
    // This would typically fetch from the backend
    // For now, we'll use session storage or default values
    const xpCounter = document.getElementById('xp-counter');
    const streakCounter = document.getElementById('streak-counter');
    
    if (xpCounter) {
        xpCounter.textContent = sessionStorage.getItem('userXP') || '0';
    }
    
    if (streakCounter) {
        streakCounter.textContent = sessionStorage.getItem('userStreak') || '0';
    }
}

function initializeLessonInteractions() {
    // Lesson node click handlers
    document.querySelectorAll('.lesson-node').forEach(node => {
        node.addEventListener('click', function() {
            if (this.classList.contains('locked')) {
                showLockedMessage();
                return;
            }
            
            if (this.classList.contains('available') || this.classList.contains('completed')) {
                const lessonId = this.dataset.lessonId;
                if (lessonId) {
                    window.location.href = `/lessons/${lessonId}`;
                }
            }
        });
    });
    
    // Exercise submission handlers
    document.querySelectorAll('.submit-answer').forEach(button => {
        button.addEventListener('click', handleExerciseSubmission);
    });
    
    // Hint button handlers
    document.querySelectorAll('.show-hint').forEach(button => {
        button.addEventListener('click', showHint);
    });
}

function handleExerciseSubmission(event) {
    const button = event.target;
    const exerciseCard = button.closest('.exercise-card');
    const exerciseId = button.dataset.exerciseId;
    const lessonId = button.dataset.lessonId;
    
    // Get the answer
    let answer = '';
    const radioInputs = exerciseCard.querySelectorAll('input[type="radio"]:checked');
    const textInput = exerciseCard.querySelector('input[type="text"]');
    
    if (radioInputs.length > 0) {
        answer = radioInputs[0].value;
    } else if (textInput) {
        answer = textInput.value.trim();
    }
    
    if (!answer) {
        showAlert('Please select or enter an answer!', 'warning');
        return;
    }
    
    // Show loading state
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Checking...';
    
    // Submit to backend
    fetch(`/lessons/${lessonId}/submit`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            exercise_id: exerciseId,
            answer: answer
        })
    })
    .then(response => response.json())
    .then(data => {
        showExerciseFeedback(exerciseCard, data);
        
        if (data.correct) {
            // Update XP counter
            updateXPCounter(data.total_xp);
            
            // Mark as completed
            button.innerHTML = '<i class="fas fa-check me-1"></i>Completed';
            button.classList.remove('btn-primary');
            button.classList.add('btn-success');
            button.disabled = true;
            
            // Show success animation
            showSuccessAnimation(exerciseCard);
        } else {
            // Re-enable button for retry
            button.disabled = false;
            button.innerHTML = '<i class="fas fa-check me-1"></i>Submit Answer';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Error submitting answer. Please try again.', 'danger');
        button.disabled = false;
        button.innerHTML = '<i class="fas fa-check me-1"></i>Submit Answer';
    });
}

function showExerciseFeedback(exerciseCard, data) {
    const feedbackDiv = exerciseCard.querySelector('.exercise-feedback');
    if (!feedbackDiv) return;
    
    feedbackDiv.style.display = 'block';
    
    const alertClass = data.correct ? 'alert-success' : 'alert-warning';
    const icon = data.correct ? 'fa-check-circle' : 'fa-exclamation-triangle';
    
    let feedbackHTML = `
        <div class="alert ${alertClass}">
            <i class="fas ${icon} me-2"></i>
            ${data.message}
    `;
    
    if (data.correct && data.xp_earned) {
        feedbackHTML += `<br><small><i class="fas fa-star me-1"></i>+${data.xp_earned} XP earned!</small>`;
    }
    
    if (data.hint && !data.correct) {
        feedbackHTML += `<br><small><strong>Hint:</strong> ${data.hint}</small>`;
    }
    
    feedbackHTML += '</div>';
    
    feedbackDiv.innerHTML = feedbackHTML;
}

function showHint(event) {
    const button = event.target;
    const hint = button.dataset.hint;
    const exerciseCard = button.closest('.exercise-card');
    const feedbackDiv = exerciseCard.querySelector('.exercise-feedback');
    
    if (feedbackDiv) {
        feedbackDiv.style.display = 'block';
        feedbackDiv.innerHTML = `
            <div class="alert alert-info">
                <i class="fas fa-lightbulb me-2"></i>
                <strong>Hint:</strong> ${hint}
            </div>
        `;
    }
}

function showLockedMessage() {
    showAlert('Complete the previous lesson to unlock this one! 🔒', 'info');
}

function showSuccessAnimation(element) {
    element.style.transform = 'scale(1.02)';
    element.style.boxShadow = '0 10px 30px rgba(88, 204, 2, 0.3)';
    
    setTimeout(() => {
        element.style.transform = 'scale(1)';
        element.style.boxShadow = '';
    }, 1000);
}

function updateXPCounter(newXP) {
    const xpCounter = document.getElementById('xp-counter');
    if (xpCounter) {
        animateCounter(xpCounter, parseInt(xpCounter.textContent), newXP);
        sessionStorage.setItem('userXP', newXP);
    }
}

function animateCounter(element, start, end) {
    const duration = 1000;
    const startTime = performance.now();
    
    function updateCounter(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const current = Math.floor(start + (end - start) * progress);
        element.textContent = current;
        
        if (progress < 1) {
            requestAnimationFrame(updateCounter);
        }
    }
    
    requestAnimationFrame(updateCounter);
}

function initializeMascot() {
    const mascot = document.getElementById('calcy-parrot');
    const speech = document.getElementById('mascot-speech');
    
    if (!mascot || !speech) return;
    
    // Random encouraging messages
    const messages = [
        "Ready to start your calculus adventure? 🧮",
        "Math is fun when you understand it! 📚",
        "Every expert was once a beginner! 🌟",
        "You've got this! Keep going! 💪",
        "Calculus is just organized common sense! 🎯",
        "Don't give up! You're doing great! 🚀",
        "Practice makes perfect! 🎓",
        "Math is the language of the universe! 🌌"
    ];
    
    // Show random message every 10 seconds
    setInterval(() => {
        const randomMessage = messages[Math.floor(Math.random() * messages.length)];
        speech.querySelector('p').textContent = randomMessage;
        speech.classList.add('show');
        
        setTimeout(() => {
            speech.classList.remove('show');
        }, 3000);
    }, 10000);
    
    // Click mascot for random message
    mascot.addEventListener('click', function() {
        const randomMessage = messages[Math.floor(Math.random() * messages.length)];
        speech.querySelector('p').textContent = randomMessage;
        speech.classList.add('show');
        
        setTimeout(() => {
            speech.classList.remove('show');
        }, 3000);
    });
}

function showAlert(message, type = 'info') {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at top of main content
    const main = document.querySelector('main');
    if (main) {
        main.insertBefore(alertDiv, main.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Export functions for global use
window.Calcuingo = {
    showAlert,
    updateXPCounter,
    animateCounter
};
