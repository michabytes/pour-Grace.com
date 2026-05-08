// Shooting stars animation
const sky = document.querySelector('.sky');

function createShootingStar() {
    const star = document.createElement('div');
    star.classList.add('shooting-star');
    star.style.top = Math.random() * window.innerHeight + 'px';
    star.style.left = Math.random() * window.innerWidth + 'px';
    star.style.animationDuration = (1 + Math.random()).toFixed(2) + 's';
    sky.appendChild(star);

    setTimeout(() => {
        star.remove();
    }, 2000);
}

// Generate constant shooting stars
setInterval(() => {
    for (let i = 0; i < 3; i++) {
        createShootingStar();
    }
}, 500);

// Audio autoplay on first click
const audio = document.getElementById('musique');
function startAudio() {
    if (audio) {
        audio.play().catch(e => console.log('Audio autoplay prevented'));
        document.removeEventListener('click', startAudio);
    }
}
document.addEventListener('click', startAudio);

// Floating hearts animation
const floatingHearts = document.querySelector('.floating-hearts');
if (floatingHearts) {
    setInterval(() => {
        const heart = document.createElement('span');
        heart.textContent = ['❤️', '💕', '💖', '💗'][Math.floor(Math.random() * 4)];
        heart.style.position = 'fixed';
        heart.style.left = Math.random() * window.innerWidth + 'px';
        heart.style.bottom = '-50px';
        heart.style.fontSize = (20 + Math.random() * 20) + 'px';
        heart.style.zIndex = '99';
        heart.style.animation = 'floatUp 3s ease-in forwards';
        document.body.appendChild(heart);
        
        setTimeout(() => {
            heart.remove();
        }, 3000);
    }, 500);
}

// Add floatUp animation
const style = document.createElement('style');
style.textContent = `
    @keyframes floatUp {
        0% {
            transform: translateY(0) rotate(0deg);
            opacity: 1;
        }
        100% {
            transform: translateY(-100vh) rotate(360deg);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
