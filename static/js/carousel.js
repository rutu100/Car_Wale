function scrollCarousel(direction) {
    const carousel = document.getElementById("carCarousel");
    if (!carousel) return;

    const scrollAmount = 260;
    carousel.scrollBy({
        left: direction * scrollAmount,
        behavior: "smooth"
    });
}
