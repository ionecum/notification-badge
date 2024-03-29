<template>
    <div class="fancy-container">
        <div class="notification-container" @click="toggleNotificationMenu">
            <a href="#" class="position-relative" >
                <i class="fa fa-bell _gray" style="font-size:24px"></i>
                <span class="my-text btnLnk">Visits</span>
                <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger _reduced">
                    {{ notificationCount }}
                </span>
            </a>
        
        <!-- Dynamic component to display notifications list -->
        <component 
            :is="showNotifications ? 'NotificationsList' : 'div'" 
            :notifications="notifications" 
            v-if="notifications.length > 0" 
            @close="closeNotificationMenu" 
        />
        <!-- <a v-if="notifications.length > 20 && showNotifications" @click="showAllNotifications" style="cursor: pointer; color: blue; text-decoration: underline;">See More</a> -->
    </div>
    </div>
</template>
<style>

</style>
<script>
//import Axios from 'axios';
import NotificationsList from './NotificationList.vue';
export default {
    data() {
        return {
            notifications: [],
            webSocket: null,
            showNotifications: false, // Flag to toggle showing notifications list
        };
    },
    computed: {
        notificationCount() {
        // Calculate the notification count based on the current state of notifications
        return this.notifications.filter(notification => !notification.fields.is_read).length;
        }
    },
    mounted() {
        document.addEventListener('click', this.handleClickOutside);
        this.$el.querySelector('.notification-container').addEventListener('click', this.handleMenuClick);
        this.establishWebSocketConnection();
    },
    beforeUnmount() {
        document.removeEventListener('click', this.handleClickOutside);
        this.$el.querySelector('.notification-container').removeEventListener('click', this.handleMenuClick);
    },
    methods: {
        toggleNotificationMenu() {
            this.showNotifications = !this.showNotifications;
        },
        closeNotificationMenu() {
            this.showNotifications = false; // Hide the notifications list
        },
        handleClickOutside(event) {
            if (!this.$el.contains(event.target)) {
                this.showNotifications = false;
            }
        },
        handleMenuClick(event) {
            event.stopPropagation(); // Prevent the click event from bubbling up
        },
        handleNotificationClick(notification) {
            notification.is_read = true; // Mark the notification as read
            // Emit an event to notify the parent component about the notification being read
            this.$emit('notification-read', notification);
        },

        async establishWebSocketConnection() {
            this.webSocket = new WebSocket('ws://127.0.0.1:8001/websocket/ws/notifications/');
            
            this.webSocket.onopen = () => {
                console.log('WebSocket connection established!');
                this.updateNotificationCount();
            };
            
            this.webSocket.onmessage = (event) => {
                //console.log("Message received:", event.data);
                
                const message = JSON.parse(event.data);
                //console.log("Event is:", event);  // Log the type field to identify the message type
                if(message.type === 'notification.update'){
                    this.notifications = message.is_read_values.map(
                        (is_read, index) => ({ 
                            fields: { is_read },
                            message: message.messages_values[index]
                            
                        }))
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
            //console.log('updateNotificationCount called!');
            // Send a message to the WebSocket server to request updated notification count
            this.webSocket.send(JSON.stringify({
                "type": "update.notification.count"  // Define a custom type to trigger the count update
            }));

        },
    },
    components: {
        NotificationsList, // Register the NotificationsList component
    },
};
</script>