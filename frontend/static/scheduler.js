let processes = [];
let processId = 1;
let table;
let savedQuantum = 0;

document.addEventListener('DOMContentLoaded', () => {
  // Initialize table
  table = new Tabulator("#processes-table", {
    layout: "fitColumns",
    columns: [
      { title: "Process ID", field: "processId" },
      { title: "Arrival Time", field: "arrivalTime" },
      { title: "Burst Time", field: "burstTime" },
      { title: "Priority", field: "priority" }
    ],
    data: processes,
  });

  // Add process
  document.getElementById('new-process-form').addEventListener('submit', e => {
    e.preventDefault();
    const arrival = Number(document.getElementById('arrival-time').value);
    const burst = Number(document.getElementById('burst-time').value);
    const priority = Number(document.getElementById('priority')?.value || 0);

    const process = {
      processId: processId++,
      arrivalTime: arrival,
      burstTime: burst,
      priority: priority
    };

    processes.push(process);
    table.setData(processes);
    e.target.reset();
  });

  // ✅ Set Quantum value
  const quantumForm = document.getElementById('quantum-form');
  if (quantumForm) {
    quantumForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const quantumInput = document.getElementById('quantum');
      const q = Number(quantumInput.value);
      if (!q || isNaN(q) || q <= 0) {
        alert("Please enter a valid quantum (positive number).");
        return;
      }
      savedQuantum = q;
      alert(`Quantum set to ${savedQuantum}`);
    });
  }

  // Run algorithm
  document.getElementById('start-btn').addEventListener('click', async () => {
    let algo = 'fcfs';
    const pageTitle = document.querySelector('h1')?.textContent?.toLowerCase();
    if (pageTitle.includes('round robin')) {
      algo = 'round-robin';
    }

    const payload = { processes };

    if (algo === 'round-robin') {
      if (!savedQuantum || isNaN(savedQuantum) || savedQuantum <= 0) {
        alert("Please set a valid Time Quantum first using the 'Set' button.");
        return;
      }
      payload.quantum = savedQuantum;
    }

    try {
      const response = await fetch(`http://localhost:5000/api/${algo}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const result = await response.json();

      if (result.chart) {
        drawGantt(result.chart);
        document.getElementById('avg-turnaround-result').textContent = `${result.averageTurnaround}s`;
        document.getElementById('avg-waiting-result').textContent = `${result.averageWaiting}s`;
      } else {
        alert('Error from server: ' + JSON.stringify(result));
      }

    } catch (err) {
      console.error('Fetch error:', err);
      alert('Failed to connect to Flask backend.');
    }
  });

  // Retry
  document.getElementById('retry-btn').addEventListener('click', () => {
    processes = [];
    processId = 1;
    savedQuantum = 0;
    table.setData([]);
    document.getElementById('chart-container').innerHTML = '';
    document.getElementById('avg-turnaround-result').textContent = '━';
    document.getElementById('avg-waiting-result').textContent = '━';
    const q = document.getElementById('quantum');
    if (q) q.value = '';
  });
});

// Gantt chart
function drawGantt(chart) {
  const container = document.getElementById('chart-container');
  container.innerHTML = '';
  chart.forEach(p => {
    const segment = document.createElement('div');
    segment.className = 'chart-segment';
    segment.style.width = (p.end - p.start) * 30 + 'px';
    segment.style.backgroundColor = randomColor();
    segment.innerHTML = `
      <p class="chart-segment-start-time">${p.start}</p>
      <p>P${p.processId}</p>
      <p class="chart-segment-end-time">${p.end}</p>
    `;
    container.appendChild(segment);
  });
}

// Color generator
function randomColor() {
  const r = Math.floor(Math.random() * 100 + 100);
  const g = Math.floor(Math.random() * 100 + 100);
  const b = Math.floor(Math.random() * 100 + 100);
  return `rgb(${r}, ${g}, ${b})`;
}
