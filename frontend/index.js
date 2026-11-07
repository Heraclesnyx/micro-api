const API_URL = "http://127.0.0.1:8000";

async function loadTasks() {
  const message = document.getElementById("message");

  try {
    const response = await fetch(`${API_URL}/tasks`);

    if (!response.ok) {
      throw new Error(`Erreur HTTP : ${response.status}`);
    }

    const tasks = await response.json();
    message.textContent = "";
    displayTasks(tasks);
  } catch (error) {
    console.error(error);
    message.textContent =
      "Impossible de charger les tâches. Vérifie que l'API est disponible.";
  }
}

function displayTasks(tasks) {
  const ul = document.getElementById("tasks");
  ul.replaceChildren();

  if (tasks.length === 0) {
    const li = document.createElement("li");
    li.textContent = "Aucune tâche";
    ul.appendChild(li);
    return;
  }

  tasks.forEach((task) => {
    const li = document.createElement("li");
    li.textContent = task.title;
    ul.appendChild(li);
  });
}

loadTasks();
