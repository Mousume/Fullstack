import { useEffect, useState } from 'react'
import './App.css'

const API_URL = 'http://localhost:5001'

function App() {
  const [users, setUsers] = useState([])
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [message, setMessage] = useState('')

  async function loadUsers() {
    const response = await fetch(`${API_URL}/users`)
    if (!response.ok) throw new Error('Could not load users')
    setUsers(await response.json())
  }

  useEffect(() => {
    loadUsers().catch(() => setMessage('Could not connect to the backend'))
  }, [])

  async function handleSubmit(event) {
    event.preventDefault()
    setMessage('')

    try {
      const response = await fetch(`${API_URL}/users`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email }),
      })

      const data = await response.json()
      if (!response.ok) throw new Error(data.error || 'Could not create user')

      setUsers((currentUsers) => [...currentUsers, data])
      setName('')
      setEmail('')
      setMessage('User saved successfully')
    } catch (error) {
      setMessage(error.message)
    }
  }

  return (
    <main className="app-shell">
      <section className="intro">
        <p className="eyebrow">PostgreSQL + Flask</p>
        <h1>Users</h1>
        <p className="description">Add a user from the frontend and store it in PostgreSQL.</p>
      </section>

      <section className="workspace">
        <form className="user-form" onSubmit={handleSubmit}>
          <h2>Add user</h2>
          <label>
            Name
            <input value={name} onChange={(event) => setName(event.target.value)} required />
          </label>
          <label>
            Email
            <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} required />
          </label>
          <button type="submit">Save user</button>
          {message && <p className="message">{message}</p>}
        </form>

        <div className="user-list">
          <div className="list-heading">
            <h2>Saved users</h2>
            <span>{users.length}</span>
          </div>
          {users.length === 0 ? (
            <p className="empty-state">No users yet.</p>
          ) : (
            <ul>
              {users.map((user) => (
                <li key={user.id}>
                  <strong>{user.name}</strong>
                  <span>{user.email}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </section>
    </main>
  )
}

export default App
