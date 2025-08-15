let currentNumber = '0';
let previousNumber = '';
let currentOperation = null;
let shouldResetDisplay = false;
let history = [];

const display = document.getElementById('display');
const historyList = document.getElementById('history-list');

function updateDisplay() {
    display.textContent = currentNumber;
}

function clearDisplay() {
    currentNumber = '0';
    previousNumber = '';
    currentOperation = null;
    updateDisplay();
}

function appendNumber(num) {
    if (shouldResetDisplay) {
        currentNumber = '';
        shouldResetDisplay = false;
    }
    
    if (currentNumber === '0') {
        currentNumber = num;
    } else {
        currentNumber += num;
    }
    updateDisplay();
}

function appendDecimal() {
    if (shouldResetDisplay) {
        currentNumber = '0';
        shouldResetDisplay = false;
    }
    
    if (!currentNumber.includes('.')) {
        currentNumber += '.';
        updateDisplay();
    }
}

function appendOperator(operator) {
    if (currentOperation !== null && !shouldResetDisplay) {
        calculate();
    }
    
    previousNumber = currentNumber;
    currentOperation = operator;
    shouldResetDisplay = true;
}

function appendFunction(func) {
    const num = parseFloat(currentNumber);
    
    fetch('/api/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            operation: func,
            a: num
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            currentNumber = data.result.toString();
            updateDisplay();
            addToHistory(`${func}(${num}) = ${data.result}`);
            shouldResetDisplay = true;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Calculation error');
    });
}

function calculate() {
    if (currentOperation === null || previousNumber === '') {
        return;
    }
    
    const a = parseFloat(previousNumber);
    const b = parseFloat(currentNumber);
    
    let operation = currentOperation;
    
    fetch('/api/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            operation: operation,
            a: a,
            b: b
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            const operatorSymbol = currentOperation;
            addToHistory(`${a} ${operatorSymbol} ${b} = ${data.result}`);
            currentNumber = data.result.toString();
            updateDisplay();
            currentOperation = null;
            previousNumber = '';
            shouldResetDisplay = true;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Calculation error');
    });
}

function addToHistory(calculation) {
    history.unshift(calculation);
    if (history.length > 10) {
        history.pop();
    }
    updateHistory();
}

function updateHistory() {
    historyList.innerHTML = '';
    history.forEach(item => {
        const div = document.createElement('div');
        div.className = 'history-item';
        div.textContent = item;
        historyList.appendChild(div);
    });
}

document.addEventListener('keydown', function(event) {
    if (event.key >= '0' && event.key <= '9') {
        appendNumber(event.key);
    } else if (event.key === '.') {
        appendDecimal();
    } else if (event.key === '+' || event.key === '-' || event.key === '*' || event.key === '/') {
        appendOperator(event.key);
    } else if (event.key === 'Enter' || event.key === '=') {
        calculate();
    } else if (event.key === 'Escape' || event.key === 'c' || event.key === 'C') {
        clearDisplay();
    }
});

setInterval(() => {
    fetch('/health')
        .then(response => response.json())
        .then(data => {
            console.log('Health check:', data);
        })
        .catch(error => {
            console.error('Health check failed:', error);
        });
}, 30000);