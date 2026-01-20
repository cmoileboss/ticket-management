import { useState, useEffect } from 'react';
import { getAllTicketsService, deleteTicketService, createTicketService } from "../services/ticket-service.jsx" ;
import { TicketCard } from './ticket-card.jsx';



export function TicketsList () 
{
    const [tickets,setTickets] = useState([]) ;
    const [loading,setLoading] = useState(true) ;
    const [error,setError] = useState(null) ;


    useEffect(() => {
        getAllTicketsService()
            .then(data => { setTickets(data.data); console.log(data.data)})
            .catch(error => setError(error))
            .finally(() => setLoading(false));
    }, []);

    if (loading) {
        return(<div id ="loading"> Chargement des tickets en cours...   </div>)
    }

    if (error) {
        return(<div id = "error" > Error </div>)
    }

    function updateTicket(ticket, new_status) {
        let new_tickets = [...tickets];
        const index = tickets.indexOf(ticket);
        new_tickets[index].status = new_status;
        setTickets(new_tickets);
    }

    function deleteTicket(ticket_to_delete) {
        deleteTicketService(ticket_to_delete.id)
            .then(data => console.log(data))
            .catch(error => console.log(error))
        
        const new_tickets = tickets.filter((ticket) => ticket.id !== ticket_to_delete.id);
        setTickets(new_tickets);
    }

    function createTicket(ticket_to_create) {
        const max_index = getMaxIndex() + 1;
        ticket_to_create.id = max_index;
        createTicketService(ticket_to_create)
            .then(data => console.log(data))
            .catch(error => console.log(error))


        let new_tickets = [...tickets];
        new_tickets.push(ticket_to_create);
        setTickets(new_tickets);
    }

    function getMaxIndex() {
        let max_index = 0
        console.log('tickets : ', tickets)
        tickets.map((ticket) => {
            if (parseInt(ticket.id) > max_index)
                max_index = parseInt(ticket.id);
        })
        console.log('max_index : ' + max_index)
        return max_index;
    }

    return(
        <div>
            <button onClick={() => createTicket({
                "title": "Ajouter un filtre par priorité",
                "description": "Permettre de filtrer les tickets par priorité (Low, Medium, High) sur la page liste.",
                "priority": "Medium",
                "status": "In progress",
                "tags": ["feature", "ux"],
                "createdAt": "2026-01-15"
            })}>Ajouter ticket</button>
            <ul>
                { tickets.map(ticket=>{
                    const deleteId = 'delete-button-' + ticket.id;
                    return (
                    <li key={ticket.id}>
                        { TicketCard(ticket, updateTicket) }
                        <button onClick={() => deleteTicket(ticket)}>Supprimer</button>
                    </li>)
                })}
            </ul>
        </div>
    )
}
//                     <button id='delete-button' onClick={deleteTicket(ticket)}>Supprimer</button>
