/*  ————————————————————————————
    Scheduler: Recommendation.js
    Shows Priority column and keeps API logic unchanged
    ———————————————————————————— */

const API_BASE = "http://127.0.0.1:5000";

/* ---------- tiny helpers ---------- */
const $ = (id) => document.getElementById(id);
const toast = (msg) => alert(msg);

let table;

/* ---------- init Tabulator ---------- */
function initTable() {
  table = new Tabulator("#processes-table", {
    layout: "fitColumns",
    reactiveData: true,
    columns: [
      { title: "PID", field: "pid", width: 70 },
      { title: "Arrival", field: "arrival_time" },
      { title: "Burst", field: "burst_time" },
      /* The Priority column is now visible by default */
      { title: "Priority", field: "priority" },
    ],
  });
}

/* ---------- backend helpers ---------- */
async function refreshTable() {
  try {
    const res = await fetch(`${API_BASE}/get_processes`);
    const data = await res.json();
    table.replaceData(data);
  } catch (err) {
    toast("Failed to fetch process table.");
    console.error(err);
  }
}

async function addProcess(arrival, burst, priority) {
  const fd = new FormData();
  fd.append("arrival_time", arrival);
  fd.append("burst_time", burst);
  /* back-end treats missing priority as 0, but we always send it */
  fd.append("priority", priority === "" ? 0 : priority);

  const res = await fetch(`${API_BASE}/add_process`, {
    method: "POST",
    body: fd,
  });

  const json = await res.json().catch(async () => {
    const txt = await res.text();
    throw new Error("Unexpected response: " + txt.slice(0, 100));
  });

  if (!res.ok) throw new Error(json.error || "Add process failed");
}

async function resetAll() {
  await fetch(`${API_BASE}/reset`, { method: "POST" });
}

async function fetchRecommendation() {
  /* 1. get current processes */
  const res = await fetch(`${API_BASE}/get_processes`);
  const data = await res.json();

  /* 2. ask Flask model for algorithm suggestion */
  const result = await fetch(`${API_BASE}/predict-algorithm`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ processes: data }),
  });

  if (!result.ok) throw new Error("Failed to get recommendation");

  const json = await result.json();
  const algoElem = $("algorithm-suggestion");
  if (algoElem) {
    algoElem.textContent = `${json.algorithm} — ${json.reason}`;
  }
}

/* ---------- DOM Ready ---------- */
document.addEventListener("DOMContentLoaded", () => {
  initTable();
  refreshTable();

  /* Add process */
  const form = $("new-process-form");
  form?.addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
      await addProcess(
        $("arrival-time").value,
        $("burst-time").value,
        $("priority").value
      );
      form.reset();
      await refreshTable();
      if ($("live")?.checked) await fetchRecommendation();
    } catch (err) {
      toast(err.message);
      console.error("Add Error:", err);
    }
  });

  /* Retry */
  $("retry-btn")?.addEventListener("click", async () => {
    await resetAll();
    $("algorithm-suggestion").textContent = "━";
    await refreshTable();
  });

  /* Start / Predict */
  $("start-btn")?.addEventListener("click", async () => {
    try {
      await fetchRecommendation();
    } catch (err) {
      toast("Could not fetch recommendation.");
      console.error(err);
    }
  });

  /* Back navigation */
  $("back-btn")?.addEventListener("click", () => history.back());
});
