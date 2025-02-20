// Global variables
let totalBudget = 0;
let expenses = [];

// Set the total budget
function setTotalBudget() {
    const budgetInput = document.getElementById('totalBudget');
    const amount = parseFloat(budgetInput.value);
    
    if (amount > 0) {
        totalBudget = amount;
        updateBudgetDisplay();
        updateCharts();
        provideBudgetSuggestions();
        budgetInput.value = '';
    } else {
        alert('Please enter a valid budget amount');
    }
}

// Add expense
function addExpense() {
    const category = document.getElementById('expenseCategory').value;
    const amount = parseFloat(document.getElementById('expenseAmount').value);
    const description = document.getElementById('expenseDescription').value;

    if (amount > 0 && description) {
        const expense = {
            category,
            amount,
            description,
            date: new Date().toLocaleDateString()
        };

        expenses.push(expense);
        updateBudgetDisplay();
        updateExpenseList();
        updateCharts();
        provideBudgetSuggestions();

        // Clear input fields
        document.getElementById('expenseAmount').value = '';
        document.getElementById('expenseDescription').value = '';
    } else {
        alert('Please enter valid expense details');
    }
}

// Update budget display
function updateBudgetDisplay() {
    const totalExpenses = calculateTotalExpenses();
    const remainingBudget = totalBudget - totalExpenses;
    const budgetUtilization = totalBudget > 0 ? (totalExpenses / totalBudget) * 100 : 0;

    document.getElementById('displayTotalBudget').textContent = `$${totalBudget.toFixed(2)}`;
    document.getElementById('displayTotalExpenses').textContent = `$${totalExpenses.toFixed(2)}`;
    document.getElementById('displayRemainingBudget').textContent = `$${remainingBudget.toFixed(2)}`;
    
    const progressBar = document.getElementById('budgetProgress');
    progressBar.style.width = `${Math.min(budgetUtilization, 100)}%`;
    progressBar.style.backgroundColor = budgetUtilization > 90 ? '#e74c3c' : '#2ecc71';
}

// Calculate total expenses
function calculateTotalExpenses() {
    return expenses.reduce((total, expense) => total + expense.amount, 0);
}

// Update expense list
function updateExpenseList() {
    const expenseList = document.getElementById('expenseList');
    expenseList.innerHTML = '';

    expenses.forEach((expense, index) => {
        const expenseElement = document.createElement('div');
        expenseElement.className = 'expense-item';
        expenseElement.innerHTML = `
            <span>${expense.date} - ${expense.category}: ${expense.description}</span>
            <span>$${expense.amount.toFixed(2)}</span>
        `;
        expenseList.appendChild(expenseElement);
    });
}

// Update charts
function updateCharts() {
    const ctx = document.getElementById('expensePieChart');
    
    if (window.pieChart) {
        window.pieChart.destroy();
    }

    const categoryTotals = {};
    expenses.forEach(expense => {
        categoryTotals[expense.category] = (categoryTotals[expense.category] || 0) + expense.amount;
    });

    window.pieChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: Object.keys(categoryTotals),
            datasets: [{
                data: Object.values(categoryTotals),
                backgroundColor: [
                    '#2ecc71',
                    '#3498db',
                    '#e74c3c',
                    '#f1c40f'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Expense Distribution'
                }
            }
        }
    });
}

// Provide budget suggestions
function provideBudgetSuggestions() {
    const totalExpenses = calculateTotalExpenses();
    const remainingBudget = totalBudget - totalExpenses;
    const suggestionsDiv = document.getElementById('budgetSuggestions');
    
    if (totalBudget === 0) {
        suggestionsDiv.innerHTML = '<p>Please set a total budget to receive suggestions.</p>';
        return;
    }

    if (totalExpenses > totalBudget) {
        suggestionsDiv.innerHTML = `
            <p>⚠️ Warning: You have exceeded your budget by $${(totalExpenses - totalBudget).toFixed(2)}</p>
            <p>Suggestions:</p>
            <ul>
                <li>Review and cut non-essential expenses</li>
                <li>Consider reallocating funds from lower-priority categories</li>
                <li>Look for cost-effective alternatives for expensive items</li>
            </ul>
        `;
    } else if ((totalExpenses / totalBudget) > 0.8) {
        suggestionsDiv.innerHTML = `
            <p>⚠️ Note: You have used ${((totalExpenses / totalBudget) * 100).toFixed(1)}% of your budget</p>
            <p>Suggestions:</p>
            <ul>
                <li>Carefully monitor remaining expenses</li>
                <li>Prioritize essential expenses</li>
                <li>Consider saving some budget for unexpected costs</li>
            </ul>
        `;
    } else {
        suggestionsDiv.innerHTML = `
            <p>✅ Your budget utilization is healthy at ${((totalExpenses / totalBudget) * 100).toFixed(1)}%</p>
            <p>Remaining budget: $${remainingBudget.toFixed(2)}</p>
        `;
    }
}

// Initialize when the page loads
document.addEventListener('DOMContentLoaded', () => {
    updateBudgetDisplay();
    updateCharts();
    provideBudgetSuggestions();
});