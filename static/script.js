// static/script.js
console.log("Script loaded!");

document.addEventListener('DOMContentLoaded', function() {
    const scanLine = document.querySelector('.scan-line');
    if (scanLine) {
        gsap.to(scanLine, {
            yPercent: 200, // Move down 200% of its height
            duration: 1.5,
            ease: "power2.inOut",
            repeat: -1, // Infinite repeat
            yoyo: true, // Go back and forth
            onUpdate: function() {
                const progress = this.progress();
                const opacity = 0.6 + Math.abs(progress - 0.5) * 0.8; // Fade in/out
                scanLine.style.opacity = opacity;
                const hue = 200 + progress * 100; // Vary hue slightly
                scanLine.style.backgroundColor = `hsla(${hue}, 70%, 50%, ${opacity})`;
            }
        });

        // Add a subtle pulsing effect to the scanning container
        const scanningAnimationContainer = document.querySelector('.scanning-animation');
        if (scanningAnimationContainer) {
            gsap.to(scanningAnimationContainer, {
                scale: 1.03,
                duration: 1,
                ease: "power1.inOut",
                repeat: -1,
                yoyo: true
            });
        }
    }

    // Example for dynamically updating the devices list (placeholder)
    const availableDevicesList = document.getElementById('available-devices');
    if (availableDevicesList) {
        // In a real application, you would fetch this data dynamically
        const devices = ["Laptop-Alpha", "Mobile-Beta", "Tablet-Gamma"];
        availableDevicesList.innerHTML = ""; // Clear initial "No devices found"
        devices.forEach(device => {
            const listItem = document.createElement('li');
            listItem.textContent = device;
            // Add a subtle animation to each device item
            gsap.fromTo(listItem, { opacity: 0, y: -10 }, { opacity: 1, y: 0, duration: 0.5, delay: devices.indexOf(device) * 0.2 });
            availableDevicesList.appendChild(listItem);
        });
    }
});