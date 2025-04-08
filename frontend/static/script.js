console.log("JS is working!");

window.onload = function () {
  loadTasks();
};

function loadTasks() {
  fetch("/tasks")
    .then((res) => res.json())
    .then((tasks) => {
      const list = document.getElementById("taskList");
      list.innerHTML = "";
      tasks.forEach((task) => {
        const li = document.createElement("li");
        li.className = "task-item";
        li.innerHTML = `
          ${task.task}
          <button class="delete-btn" onclick="deleteTask('${task.id}')">Delete</button>
        `;
        list.appendChild(li);
      });
    });
}

function addTask() {
  const taskInput = document.getElementById("taskInput");
  const task = taskInput.value.trim();
  if (task === "") return;
  fetch("/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ task: task }),
  }).then(() => {
    taskInput.value = "";
    loadTasks();
  });
}

function deleteTask(id) {
  fetch(`/tasks/${id}`, { method: "DELETE" }).then(() => loadTasks());
}
