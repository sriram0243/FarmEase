// ==========================================================================
// FARMEASE - HOMEPAGE & GLOBAL SCRIPT
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {
    // 1. Counter Animation for Homepage Statistics
    const counters = document.querySelectorAll('.stat-number');
    
    counters.forEach(counter => {
        const updateCount = () => {
            const target = +counter.getAttribute('data-target');
            const count = +counter.innerText;
            const speed = 40;
            const increment = Math.max(1, Math.ceil(target / speed));

            if (count < target) {
                counter.innerText = Math.min(target, count + increment);
                setTimeout(updateCount, 35);
            } else {
                counter.innerText = target;
            }
        };

        // Trigger animation when counters are in viewport
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    updateCount();
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        observer.observe(counter);
    });

    // 2. Featured Equipment Preview Data
    const previewEquipments = [
        {
            id: 1,
            name: "John Deere 5310",
            image: "tractor.png",
            rating: "4.9",
            reviews: 125,
            hp: "55 HP",
            fuel: "Diesel",
            location: "Coimbatore",
            price: "₹1,200",
            badge: "Most Booked"
        },
        {
            id: 2,
            name: "Mahindra Arjun 605",
            image: "tractor.png",
            rating: "4.8",
            reviews: 96,
            hp: "60 HP",
            fuel: "Diesel",
            location: "Erode",
            price: "₹1,400",
            badge: "Top Rated"
        },
        {
            id: 3,
            name: "Kubota Harvester",
            image: "harvester.png",
            rating: "4.7",
            reviews: 88,
            hp: "75 HP",
            fuel: "Diesel",
            location: "Salem",
            price: "₹3,500",
            badge: "Premium"
        }
    ];

    const container = document.getElementById("equipmentPreviewContainer");
    if (container) {
        container.innerHTML = previewEquipments.map(item => `
            <div class="col-lg-4 col-md-6 mb-4">
                <div class="equipment-card">
                    <div class="card-top">
                        <span class="badge-tag">🔥 ${item.badge}</span>
                        <i class="fa-regular fa-heart heart-icon" onclick="toggleHeart(this)"></i>
                    </div>
                    
                    <div class="equipment-img-box">
                        <img src="/static/images/equipment/${item.image}" alt="${item.name}" class="img-fluid">
                    </div>

                    <h4 class="equipment-title">${item.name}</h4>
                    
                    <div class="equipment-rating">
                        ⭐ ${item.rating} <span class="text-muted font-weight-normal">(${item.reviews} reviews)</span>
                    </div>

                    <div class="equipment-meta">
                        <span>⚙️ ${item.hp}</span>
                        <span>⛽ ${item.fuel}</span>
                        <span>📍 ${item.location}</span>
                    </div>

                    <div class="equipment-price">
                        ${item.price}<small>/day</small>
                    </div>

                    <div class="card-actions">
                        <a href="/equipment/${item.id}" class="btn-card-secondary">View Details</a>
                        <a href="/booking/${item.id}" class="btn-card-primary">Book Now</a>
                    </div>
                </div>
            </div>
        `).join('');
    }
});

function toggleHeart(element) {
    element.classList.toggle('fa-regular');
    element.classList.toggle('fa-solid');
    element.classList.toggle('active');
}