async function fetchDueDiligence() {
    const ticker = document.getElementById('stock-ticker').value.trim();
    if (!ticker) {
        alert('Please enter a stock ticker.');
        return;
    }

    const loadingElement = document.getElementById('loading');
    loadingElement.style.display = 'block'; // Show loading animation

    try {
        console.log(`Fetching due diligence for ${ticker}...`);
        const response = await fetch(`http://127.0.0.1:8000/due_diligence/${ticker}`, {
            method: 'GET',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        console.log('Response status:', response.status);
        console.log('Response headers:', response.headers);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Received data:', data);

        if (data && data.DD && data.DD.due_diligence) {
            displayDueDiligence(data.DD.due_diligence);
        } else {
            throw new Error('Invalid response format');
        }
    } catch (error) {
        console.error('Error fetching due diligence:', error);
        alert('Failed to fetch due diligence. Please try again later.');
    } finally {
        loadingElement.style.display = 'none'; // Hide loading animation
    }
}

function displayDueDiligence(dueDiligence) {
    const sectionsContainer = document.getElementById('due-diligence-sections');
    sectionsContainer.innerHTML = ''; // Clear previous results

    console.log('Received due diligence:', dueDiligence);

    if (dueDiligence && typeof dueDiligence === 'object') {
        for (let section in dueDiligence) {
            const sectionElement = document.createElement('div');
            sectionElement.className = 'section';
            sectionElement.innerHTML = `<h2>${section}</h2><div class="section-content">${dueDiligence[section]}</div>`;
            sectionElement.querySelector('h2').onclick = function () {
                const content = this.nextElementSibling;
                content.style.display = content.style.display === 'block' ? 'none' : 'block';
            };
            sectionsContainer.appendChild(sectionElement);
        }
    } else {
        sectionsContainer.innerHTML = '<p>Invalid data format received</p>';
    }
}
