<template>
    <div class="fancy-container">
        <div class="notification-container" @click="toggleNotificationMenu">
            <a href="#" class="position-relative" >
                <i class="fa fa-bell _gray" style="font-size:24px"></i>
                <span class="my-text btnLnk">Visits</span>
                <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger _reduced" :class="{ 'hidden': !notificationCount }">
                    {{ notificationCount }}
                </span>
            </a>
            <!-- In Vue.js, the @ symbol is a shorthand for the v-on directive, which is used to listen to events emitted by child components. Whti @mark-as-read="handleMarkAsRead", we are listening for an event named mark-as-read emitted by the child component and then call the handleMarkAsRead method defined in the parent component when that event is triggered. -->
            <component 
                :is="showNotifications ? 'NotificationsList' : 'div'" 
                :notifications="notifications" 
                v-if="notifications.length > 0" 
                @close="closeNotificationMenu" 
                @mark-as-read="handleMarkAsRead"
                @mark-all-read="handleMarkAllRead"
            />
        </div>
    </div>
</template>
<style>
    .notification-container {
        position: relative;
        display: inline-block;
    }
    .my-text {
        margin-left: 5px; /* Adjust as needed */
    }
    .hidden {
        display: none;
    }
</style>
<script>
import NotificationsList from './NotificationList.vue';
export default {
    data() {
        return {
            notifications: [],
            webSocket: null,
            showNotifications: false, // Flag to toggle showing notifications list
        };
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
            //console.log("Notification count:" + this.notificationCount)
            if(this.notificationCount > 0){
                this.webSocket.send(JSON.stringify({
                    "type": "mark.all.seen"
                }));
            }
        },
        /* This method is called when the user clicks on a single notification to mark it as read */
        handleMarkAsRead(id){
            //console.log("The notification id is "+id);
            this.webSocket.send(JSON.stringify({
                "type": "mark.one.read",
                "id":id
            }));
        },
        handleMarkAllRead(){
            console.log("time to call the server!");
            
            this.webSocket.send(JSON.stringify({
                "type": "mark.all.read"
            }));
        },
        closeNotificationMenu() {
            this.showNotifications = false; // Hide the notifications list
        },
        /* The notification list must close when the user clicks outside it */
        handleClickOutside(event) {
            if (!this.$el.contains(event.target)) {
                this.showNotifications = false;
            }
        },
        handleMenuClick(event) {
            event.stopPropagation(); // Prevent the click event from bubbling up
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
                console.log(message);
                
                if(message.type === 'notification.update'){
                    this.notificationCount = message.count;
                    this.notifications = message.notifications.map(notification => ({
                        id: notification.id,
                        is_read: notification.is_read,
                        message: notification.message
                    }));
                    //console.log(this.notifications);
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