import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { TicketsList } from './components/ticket-list'

function App() {
  

  return (
    <>
      <h1>Gestion de tickets</h1>
      <TicketsList/>
    </>
  )
}

export default App
