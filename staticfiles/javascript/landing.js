document.addEventListener("scroll", function () {
    const heroElements = document.querySelectorAll(".hero-section .Intro, .hero-section h2, .hero-section p, .Intro a, .right img");
    heroElements.forEach((element) => {
        if (window.scrollY > 100) {
            element.style.animation = "fadeOutDown 1s ease forwards";
        } else {
            element.style.animation = "fadeInUp 1s ease forwards";
        }
    });
});
