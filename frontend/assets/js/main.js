window.addEventListener('DOMContentLoaded', () => {
    document.getElementById('imageSection').style.opacity = '1';
    document.getElementById('imageSection').style.transform = 'translateX(0)';
    document.getElementById('textSection').style.opacity = '1';
    document.getElementById('textSection').style.transform = 'translateX(0)';
});


function setupAnimations() {
    const features = document.querySelectorAll('.feature');

    const observerOptions = {
        root: null, // Use the viewport as the root
        rootMargin: '0px',
        threshold: 0.1 // Trigger when 10% of the element is visible
    };

    const observerCallback = (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            } else {
                entry.target.classList.remove('visible');
            }
        });
    };

    const observer = new IntersectionObserver(observerCallback, observerOptions);

    features.forEach(feature => {
        observer.observe(feature);
    });
}


function setupAnimationsTeam() {
    const teamMembers = document.querySelectorAll('.team-member');

    const observerOptions = {
        root: null, // Use the viewport as the root
        rootMargin: '0px',
        threshold: 0.1 // Trigger when 10% of the element is visible
    };

    const observerCallback = (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            } else {
                entry.target.classList.remove('visible');
            }
        });
    };

    const observer = new IntersectionObserver(observerCallback, observerOptions);

    teamMembers.forEach(member => {
        observer.observe(member);
    });
}
