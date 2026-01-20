import { updateStatusService } from '../services/ticket-service';


export function TicketCard(ticket, updateTicketinList) {

    const selectId = `select-status-${ticket.id}`;
    const statusId = `status-${ticket.id}`;

    async function updateTicket() {
        const selectObject = document.getElementById(selectId);
        const selectedStatus = selectObject.options[selectObject.selectedIndex].value;
        updateStatusService(ticket.id, selectedStatus)
            .then(data => {
                updateTicketinList(ticket, selectedStatus);
            })
            .catch(error => console.log(error));
    }

    return (
        <div id={ticket.id}>
            id : {ticket.id}<br/>
            title : {ticket.title}<br/>
            description : {ticket.description}<br/>
            priority : {ticket.pritority}<br/>
            status : {ticket.status}<br/>
            tags : { ticket.tags.join(', ')}<br/>
            createdAt : {ticket.createdAt}<br/>
            <select id={selectId}>
                <option value="open">Open</option>
                <option value="in progress">In progress</option>
                <option value="close">Close</option>
            </select>
            <button onClick={updateTicket}>Mettre à jour le statut</button>
        </div>
    )
} 
