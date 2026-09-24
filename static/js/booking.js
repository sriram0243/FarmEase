// Booking & Availability Calendar Interaction Script
document.addEventListener('DOMContentLoaded', () => {
    const startDateInput = document.getElementById('startDateInput');
    const endDateInput = document.getElementById('endDateInput');
    const priceCalculationBox = document.getElementById('priceCalculationBox');
    const selectedDaysText = document.getElementById('selectedDaysText');
    const totalPriceText = document.getElementById('totalPriceText');
    const bookNowBtn = document.getElementById('bookNowBtn');

    const todayStr = new Date().toISOString().split('T')[0];
    if (startDateInput) startDateInput.min = todayStr;
    if (endDateInput) endDateInput.min = todayStr;

    function calculateTotal() {
        if (!startDateInput || !endDateInput) return;
        const startVal = startDateInput.value;
        const endVal = endDateInput.value;

        if (startVal && endVal) {
            const start = new Date(startVal);
            const end = new Date(endVal);

            if (end < start) {
                if (priceCalculationBox) priceCalculationBox.classList.add('d-none');
                return;
            }

            const diffTime = Math.abs(end - start);
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
            const total = diffDays * (typeof equipmentPrice !== 'undefined' ? equipmentPrice : 1000);

            if (selectedDaysText) selectedDaysText.innerText = `${diffDays} day${diffDays > 1 ? 's' : ''}`;
            if (totalPriceText) totalPriceText.innerText = `₹${total.toLocaleString('en-IN')}`;
            if (priceCalculationBox) priceCalculationBox.classList.remove('d-none');
        } else {
            if (priceCalculationBox) priceCalculationBox.classList.add('d-none');
        }
    }

    if (startDateInput) {
        startDateInput.addEventListener('change', () => {
            endDateInput.min = startDateInput.value;
            if (endDateInput.value && endDateInput.value < startDateInput.value) {
                endDateInput.value = startDateInput.value;
            }
            calculateTotal();
        });
    }

    if (endDateInput) {
        endDateInput.addEventListener('change', calculateTotal);
    }

    // Auto calculate if dates preloaded
    calculateTotal();
});
