document.addEventListener('DOMContentLoaded', () => {
    // Score distribution chart
    const scoreCtx = document.getElementById('scoreChart').getContext('2d');
    const scoreChart = new Chart(scoreCtx, {
        type: 'bar',
        data: {
            labels: ['0-20', '21-40', '41-60', '61-80', '81-100'],
            datasets: [{
                label: 'Number of Quizzes Taken',
                data: [10, 25, 45, 60, 30], // Replace these values with actual data
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Category performance chart
    const categoryCtx = document.getElementById('categoryChart').getContext('2d');
    const categoryChart = new Chart(categoryCtx, {
        type: 'doughnut',
        data: {
            labels: ['Category 1', 'Category 2', 'Category 3'], // Replace these with actual categories
            datasets: [{
                data: [50, 30, 20], // Replace these values with actual data
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 205, 86, 0.2)',
                    'rgba(54, 162, 235, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 205, 86, 1)',
                    'rgba(54, 162, 235, 1)'
                ],
                borderWidth: 1
            }]
        }
    });
});
