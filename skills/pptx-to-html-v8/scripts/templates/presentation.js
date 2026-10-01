function applyAutoFit() {
    const containers = document.querySelectorAll('.autofit-container');
    containers.forEach(container => {
        let iterations = 0;
        while ((container.scrollHeight > container.clientHeight || container.scrollWidth > container.clientWidth) && iterations < 50) {
            const spans = container.querySelectorAll('span');
            let changed = false;
            spans.forEach(span => {
                const style = window.getComputedStyle(span);
                const currentSize = parseFloat(style.fontSize);
                if (currentSize > 8) {
                    span.style.fontSize = (currentSize - 1) + 'px';
                    changed = true;
                }
            });
            if (!changed) break;
            iterations++;
        }
    });
}
window.addEventListener('load', () => { setTimeout(applyAutoFit, 500); });

function resizeContainer() {
    const container = document.getElementById('slide-container');
    const scaleX = window.innerWidth / {{SLIDE_W}};
    const scaleY = window.innerHeight / {{SLIDE_H}};
    const scale = Math.min(scaleX, scaleY) * 0.95;
    container.style.transform = `scale(${scale})`;
}
window.addEventListener('resize', resizeContainer);
resizeContainer();

const slides = document.querySelectorAll('.slide');
let currentSlideIdx = 0;
let currentStep = 0;
const slideIndicator = document.getElementById('slide-indicator') || {innerText:''};
const stepIndicator = document.getElementById('step-indicator') || {innerText:''};

function updateView() {
    slides.forEach((slide, idx) => {
        if (idx === currentSlideIdx) {
            slide.classList.add('active');
            const maxStep = parseInt(slide.getAttribute('data-max-step') || 0);
            slideIndicator.innerText = `Slide ${currentSlideIdx + 1} / ${slides.length}`;
            stepIndicator.innerText = `Step ${currentStep} / ${maxStep}`;

            const stepElements = slide.querySelectorAll('[class*="step-"]');
            stepElements.forEach(el => {
                const stepMatch = el.className.match(/step-(\d+)/);
                const step = stepMatch ? parseInt(stepMatch[1]) : 0;
                if (step > 0) {
                    if (step <= currentStep) {
                        el.classList.remove('hidden-step');
                    } else {
                        el.classList.add('hidden-step');
                    }
                }
            });
        } else {
            slide.classList.remove('active');
        }
    });
}

function next() {
    const currentSlide = slides[currentSlideIdx];
    const maxStep = parseInt(currentSlide.getAttribute('data-max-step') || 0);

    if (currentStep < maxStep) {
        currentStep++;
        updateView();
    } else if (currentSlideIdx < slides.length - 1) {
        currentSlideIdx++;
        currentStep = 0;
        updateView();
    }
}

function prev() {
    if (currentStep > 0) {
        currentStep--;
        updateView();
    } else if (currentSlideIdx > 0) {
        currentSlideIdx--;
        currentStep = parseInt(slides[currentSlideIdx].getAttribute('data-max-step') || 0);
        updateView();
    }
}

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        window.location.href = '../../index.html';
    } else if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') {
        next();
    } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        prev();
    }
});

document.getElementById('slide-container').addEventListener('click', (e) => {
    next();
});

updateView();
