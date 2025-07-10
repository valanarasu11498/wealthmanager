// Chart.js configuration for dashboard charts
document.addEventListener('DOMContentLoaded', function() {
    // Initialize charts
    initCategoryChart();
    initAccountChart();
});

function initCategoryChart() {
    const ctx = document.getElementById('categoryChart');
    if (!ctx) return;

    // Fetch category data
    fetch('/api/category_data')
        .then(response => response.json())
        .then(data => {
            const labels = Object.keys(data);
            const values = Object.values(data);
            
            if (labels.length === 0) {
                ctx.getContext('2d').fillText('No spending data available', 10, 50);
                return;
            }

            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: values,
                        backgroundColor: [
                            '#FF6384',
                            '#36A2EB',
                            '#FFCE56',
                            '#4BC0C0',
                            '#9966FF',
                            '#FF9F40',
                            '#FF6384',
                            '#C9CBCF',
                            '#4BC0C0',
                            '#FF6384'
                        ],
                        borderWidth: 2,
                        borderColor: '#333'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'right',
                            labels: {
                                boxWidth: 12,
                                padding: 8,
                                usePointStyle: true
                            }
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const label = context.label || '';
                                    const value = context.parsed || 0;
                                    return `${label}: $${value.toFixed(2)}`;
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error loading category data:', error);
            ctx.getContext('2d').fillText('Error loading data', 10, 50);
        });
}

function initAccountChart() {
    const ctx = document.getElementById('accountChart');
    if (!ctx) return;

    // Fetch account data
    fetch('/api/account_data')
        .then(response => response.json())
        .then(data => {
            const labels = Object.keys(data);
            const values = Object.values(data);
            
            if (labels.length === 0) {
                ctx.getContext('2d').fillText('No account data available', 10, 50);
                return;
            }

            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Balance',
                        data: values,
                        backgroundColor: values.map(value => value >= 0 ? '#36A2EB' : '#FF6384'),
                        borderColor: values.map(value => value >= 0 ? '#36A2EB' : '#FF6384'),
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return '$' + value.toFixed(2);
                                }
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const value = context.parsed.y || 0;
                                    return `Balance: $${value.toFixed(2)}`;
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error loading account data:', error);
            ctx.getContext('2d').fillText('Error loading data', 10, 50);
        });
}
