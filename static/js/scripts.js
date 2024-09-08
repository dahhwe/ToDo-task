document.addEventListener('DOMContentLoaded', () => {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('new-completion-date').value = today;
    document.getElementById('new-completion-date').setAttribute('min', today);
});

function formatDateForDisplay(dateString) {
    const date = new Date(dateString);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    return `${day} ${month} ${year}`;
}

function sortTasksByDate(tasks) {
    return tasks.sort((a, b) => new Date(a.completion_date) - new Date(b.completion_date));
}

async function fetchTasks() {
    const response = await fetch('/todos/');
    const tasks = await response.json();
    const sortedTasks = sortTasksByDate(tasks);
    const tasksDiv = document.getElementById('tasks');
    tasksDiv.innerHTML = '';
    sortedTasks.forEach(task => {
        const taskDiv = document.createElement('div');
        taskDiv.className = 'todo' + (task.completed ? ' completed' : '');
        taskDiv.innerHTML = `
            <div class="task-info">
                <span class="title">${task.title}</span>
                <span>${task.description}</span>
                <span class="date">${formatDateForDisplay(task.completion_date)}</span>
            </div>
            <div>
                <button class="edit" onclick="editTask(${task.id})">Edit</button>
                <button class="delete" onclick="deleteTask(${task.id})">Delete</button>
                <input type="checkbox" class="complete" onclick="toggleComplete(${task.id}, ${task.completed})" ${task.completed ? 'checked' : ''}>
            </div>
        `;
        tasksDiv.appendChild(taskDiv);
    });
}

async function addTask() {
    const title = document.getElementById('new-task').value;
    const description = document.getElementById('new-description').value;
    const completion_date = document.getElementById('new-completion-date').value;

    if (!title.trim() || !description.trim()) {
        alert('Title and description are required.');
        return;
    }

    const today = new Date().toISOString().split('T')[0];
    if (new Date(completion_date) < new Date(today)) {
        alert('Completion date cannot be in the past.');
        return;
    }

    await fetch('/todos/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({title, description, completion_date, completed: false})
    });

    document.getElementById('new-task').value = '';
    document.getElementById('new-description').value = '';
    document.getElementById('new-completion-date').value = today;
    fetchTasks();
}

let currentEditId = null;

function openEditPopup(task) {
    currentEditId = task.id;
    document.getElementById('edit-title').value = task.title;
    document.getElementById('edit-description').value = task.description;
    document.getElementById('edit-completion-date').value = task.completion_date;
    document.getElementById('edit-popup').style.display = 'block';
}

function closePopup() {
    document.getElementById('edit-popup').style.display = 'none';
}

async function submitEditForm(event) {
    event.preventDefault();
    const newTitle = document.getElementById('edit-title').value;
    const newDescription = document.getElementById('edit-description').value;
    const newCompletionDate = document.getElementById('edit-completion-date').value;

    if (!newTitle.trim() || !newDescription.trim()) {
        alert('Title and description are required.');
        return;
    }

    const today = new Date().toISOString().split('T')[0];
    if (new Date(newCompletionDate) < new Date(today)) {
        alert('Completion date cannot be in the past.');
        return;
    }

    await fetch(`/todos/${currentEditId}`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            title: newTitle,
            description: newDescription,
            completion_date: newCompletionDate,
            completed: false
        })
    });

    closePopup();
    fetchTasks();
}

async function editTask(id) {
    const response = await fetch(`/todos/${id}`);
    const task = await response.json();
    openEditPopup(task);
}

async function deleteTask(id) {
    await fetch(`/todos/${id}`, {method: 'DELETE'});
    fetchTasks();
}

async function toggleComplete(id, completed) {
    const payload = {completed: !completed};
    console.log('Payload:', payload);

    try {
        const response = await fetch(`/todos/${id}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error updating task:', errorData);
            alert('Failed to update task. Please try again.');
            return;
        }

        console.log('Response:', await response.json());
        fetchTasks();
    } catch (error) {
        console.error('Error during fetch operation:', error);
        alert('An error occurred. Please try again.');
    }
}


fetchTasks();