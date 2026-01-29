import { updateStatusService } from '../services/ticket-service';
import './ticket-card.css';

export function TicketCard(ticket, updateTicketinList, deleteTicket) {

    const selectId = `select-status-${ticket.id}`;
    const statusId = `status-${ticket.id}`;

    async function updateTicket() {
        const selectObject = document.getElementById(selectId);
        const selectedStatus = selectObject.options[selectObject.selectedIndex].value;
        console.log('Updating ticket id ', ticket.id, ' to status ', selectedStatus);
        updateStatusService(ticket.id, selectedStatus)
            .then(data => {
                updateTicketinList(ticket, selectedStatus);
            })
            .catch(error => console.log(error));
    }

    return (
        <div id={ticket.id} className="ticket-card" data-priority={ticket.priority.toLowerCase()}>
            <h1>{ticket.title}</h1>
            <p><strong>Description :</strong> {ticket.description}</p>
            <p><strong>Priorité :</strong> {ticket.priority}</p>
            <p><strong>Status :</strong> <span className={`status-badge status-${ticket.status.replace(' ', '-')}`}>{ticket.status}</span></p>
            <p><strong>Tags :</strong> {ticket.tags.join(', ')}</p>
            <p><strong>Date de création :</strong> {ticket.createdAt}</p>
            <select id={selectId}>
                <option value="open">Open</option>
                <option value="in progress">In Progress</option>
                <option value="close">Close</option>
            </select>
            <button onClick={updateTicket}>Mettre à jour le statut</button>
            <button onClick={() => deleteTicket(ticket)} className="delete-button">Supprimer</button>
        </div>
    )
} 
