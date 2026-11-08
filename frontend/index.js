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

function addTask() {
  const taskTitle = document.getElementById("task-title");
  const message = document.getElementById("message");

  fetch(`${API_URL}/tasks`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ title: taskTitle.value }),
  })
    .then((response) => {
      if (!response.ok) {
        const error = new Error(`Erreur HTTP : ${response.status}`);
        error.status = response.status;
        throw error;
      }
      message.textContent = "";
      return response.json();
    })
    .then(() => {
      taskTitle.value = "";
      loadTasks();
    })
    .catch((error) => {
      console.error(error);
      if (error.status === 422) {
        message.textContent = "Le titre de la tâche ne peut pas être vide.";
      } else {
        message.textContent =
          "Impossible d'ajouter la tâche. Vérifie que l'API est disponible.";
      }
    });
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

document.getElementById("add-task").addEventListener("click", addTask);

loadTasks();
