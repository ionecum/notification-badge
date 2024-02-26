<template>
    <div class="fancy-container">
        <a href="#" class="position-relative">
            <i class="fa fa-bell _gray" style="font-size:24px"></i>
            <span class="my-text btnLnk">Visits</span>
            <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger _reduced">
                {{ notificationCount }}
            </span>
        </a>
    </div>
</template>
<script>
//import Axios from 'axios';

export default {
    data() {
        return {
            notifications: [],
            webSocket: null
        };
    },
    computed: {
        notificationCount() {
        // Calculate the notification count based on the current state of notifications
        return this.notifications.filter(notification => !notification.fields.is_read).length;
        }
    },
    mounted() {
        this.establishWebSocketConnection();
    },
    methods: {
        async establishWebSocketConnection() {
            this.webSocket = new WebSocket('ws://127.0.0.1:8001/websocket/ws/notifications/', 'echo-protocol');
            
            this.webSocket.onopen = () => {
                console.log('WebSocket connection established!');
                this.updateNotificationCount();
            };
            
            this.webSocket.onmessage = (event) => {
                console.log("Message received:", event.data);
                const message = JSON.parse(event.data);
                console.log("Received type:", message.type);  // Log the type field to identify the message type
                if(message.type === 'notification.update'){
                    this.notifications = message.is_read_values.map(is_read => ({ fields: { is_read } }));
                }else{
                    console.log("Notification count was not updated!")
                }

            };

            this.webSocket.onclose = () => {
                console.log('WebSocket connection closed.');
            // implement reconnect logic if desired
            };
        },
        updateNotificationCount() {
            console.log('updateNotificationCount called!');
            // Send a message to the WebSocket server to request updated notification count
            this.webSocket.send(JSON.stringify({
                "type": "update.notification.count"  // Define a custom type to trigger the count update
            }));

        },
    },
};
</script>