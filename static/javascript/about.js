const isElementInViewport = (el) => {
    const rect = el.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
};

const fadeInElements = () => {
    const elements = document.querySelectorAll('.fade-in');
    elements.forEach((el) => {
        if (isElementInViewport(el)) {
            el.classList.add('visible');
        }
    });
};

window.addEventListener('scroll', fadeInElements);

document.addEventListener('DOMContentLoaded', fadeInElements);

