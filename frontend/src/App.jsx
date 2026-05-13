import React, { useState, useEffect } from 'react';
import { fetchTasks, createTask, updateTask, toggleTaskStatus, deleteTask } from './services/api';

function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');
  const [editingId, setEditingId] = useState(null);
  const [editTitle, setEditTitle] = useState('');
  const [editDesc, setEditDesc] = useState('');

  // Fetch tasks on load
  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      const data = await fetchTasks();
      setTasks(data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!title.trim()) {
      setError('Title cannot be empty');
      return;
    }
    setError('');

    try {
      const newTask = await createTask({ title: title.trim(), description: description.trim() });
      setTasks([newTask, ...tasks]);
      setTitle('');
      setDescription('');
    } catch (err) {
      console.error(err);
    }
  };

  const handleToggle = async (id) => {
    try {
      const updated = await toggleTaskStatus(id);
      setTasks(tasks.map(t => t.id === id ? updated : t));
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await deleteTask(id);
        setTasks(tasks.filter(t => t.id !== id));
      } catch (err) {
        console.error(err);
      }
    }
  };

  const startEdit = (task) => {
    setEditingId(task.id);
    setEditTitle(task.title);
    setEditDesc(task.description || '');
  };

  const cancelEdit = () => {
    setEditingId(null);
    setEditTitle('');
    setEditDesc('');
  };

  const handleSaveEdit = async (id, status) => {
    if (!editTitle.trim()) {
      alert('Title cannot be empty');
      return;
    }
    try {
      const updated = await updateTask(id, { 
        title: editTitle.trim(), 
        description: editDesc.trim(),
        status
      });
      setTasks(tasks.map(t => t.id === id ? updated : t));
      setEditingId(null);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="app-container">
      <h1 className="header-title">Task Flow</h1>
      
      <form className="task-form" onSubmit={handleCreate}>
        <div className="input-group">
          <input
            type="text"
            placeholder="What needs to be done?"
            value={title}
            onChange={(e) => {
              setTitle(e.target.value);
              if (error) setError('');
            }}
          />
          {error && <span className="error-message">{error}</span>}
        </div>
        <div className="input-group">
          <textarea
            placeholder="Add a description (optional)"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows="3"
          />
        </div>
        <button type="submit" className="btn-submit">Add Task</button>
      </form>

      <div className="task-list">
        {tasks.map(task => (
          <div key={task.id} className={`task-card ${task.status === 'completed' ? 'completed' : ''}`}>
            
            <div className="task-content">
              <div className="checkbox-container">
                <input
                  type="checkbox"
                  className="task-checkbox"
                  checked={task.status === 'completed'}
                  onChange={() => handleToggle(task.id)}
                />
              </div>

              {editingId === task.id ? (
                <div className="edit-form">
                  <input
                    type="text"
                    className="edit-input"
                    value={editTitle}
                    onChange={(e) => setEditTitle(e.target.value)}
                    autoFocus
                  />
                  <textarea
                    className="edit-input"
                    value={editDesc}
                    onChange={(e) => setEditDesc(e.target.value)}
                    rows="3"
                  />
                  <div className="edit-actions">
                    <button className="btn-small btn-save" onClick={() => handleSaveEdit(task.id, task.status)}>Save</button>
                    <button className="btn-small btn-cancel" onClick={cancelEdit}>Cancel</button>
                  </div>
                </div>
              ) : (
                <div className="task-details">
                  <h3 className="task-title">{task.title}</h3>
                  {task.description && <p className="task-desc">{task.description}</p>}
                </div>
              )}
            </div>

            {editingId !== task.id && (
              <div className="task-actions">
                <button className="btn-icon btn-edit" onClick={() => startEdit(task)} title="Edit">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                  </svg>
                </button>
                <button className="btn-icon btn-delete" onClick={() => handleDelete(task.id)} title="Delete">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="3 6 5 6 21 6"></polyline>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    <line x1="10" y1="11" x2="10" y2="17"></line>
                    <line x1="14" y1="11" x2="14" y2="17"></line>
                  </svg>
                </button>
              </div>
            )}
            
          </div>
        ))}
        {tasks.length === 0 && (
          <div style={{ textAlign: 'center', color: 'var(--text-secondary)', padding: '2rem' }}>
            No tasks yet. Create one above!
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
