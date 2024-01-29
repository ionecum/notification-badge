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
            };
        
            this.webSocket.onmessage = (event) => {
                const newNotification = JSON.parse(event.data);
                // Update the notification array with the new notification
                this.notifications.push(newNotification);
                
                console.log('Updated Notifications:', this.notifications);
            };

            this.webSocket.onclose = () => {
                console.log('WebSocket connection closed.');
            // implement reconnect logic if desired
            };
        },
    },
};
</script>
