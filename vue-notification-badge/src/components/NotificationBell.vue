<template>
    <div class="fancy-container">
        <div class="notification-container" @click="toggleNotificationMenu">
            <a href="#" class="position-relative" >
                <i class="fa fa-bell _gray" style="font-size:24px"></i>
                <span class="my-text btnLnk">{{ bellText }}</span>
                <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger _reduced" :class="{ 'hidden': !notificationCount }">
                    {{ notificationCount }}
                </span>
            </a>
            <!-- In Vue.js, the @ symbol is a shorthand for the v-on directive, which is used to listen to events emitted
            by child components. With @mark-as-read="handleMarkAsRead", we are listening for an event named mark-as-read
            emitted by the child component and then call the handleMarkAsRead method defined in the parent component when
            that event is triggered. -->
            <notifications-list
                v-show="showNotifications"
                :notifications="notifications"
                @mark-as-read="handleMarkAsRead"
                @mark-all-read="handleMarkAllRead"
            />
        </div>
    </div>
</template>
<script>
import NotificationsList from './NotificationList.vue';

export default {
    components: {
        NotificationsList, // Register the NotificationsList component
    },
    // notificationType is defined in main.js
    props: ['notificationType'],
    data() {
        return {
            notificationCount: 0,
            notifications: [],
            webSocket: null,
            showNotifications: false, // Flag to toggle showing notifications list
        };
    },
    computed: {
        bellText() {
          const texts = {
            'VISIT': 'Visits',
            'TEASE': 'Teases',
            'MESSAGE': 'Messages',
            'general': 'All Notifications',
          }
          return texts[this.notificationType] || "";
        }
    },
    mounted() {
        console.log("Notification type in NotificationBell:" + this.notificationType); // This should log the notificationType
        document.addEventListener('click', this.handleClickOutside);
        this.establishWebSocketConnection();
    },
    beforeUnmount() {
        document.removeEventListener('click', this.handleClickOutside);
    },
    methods: {
        /* The notification list must close when the user clicks outside it */
        handleClickOutside(event) {
            if (!this.$el.contains(event.target)) {
                this.showNotifications = false;
            }
        },
        async establishWebSocketConnection() {
            this.webSocket = new WebSocket('ws://127.0.0.1:8001/websocket/ws/notifications/');
            
            this.webSocket.onopen = () => {
                console.log('WebSocket connection established!');
                this.updateNotificationCount();
            };
            this.webSocket.onmessage = (event) => {
                const message = JSON.parse(event.data);
                console.log(message);
                
                if((message.type === 'notification.update' && this.notificationType === 'general') ||
                    (message.type === 'notification.update.' + this.notificationType)) {
                    this.notificationCount = message.count;
                    this.notifications = message.notifications.map(notification => ({
                        id: notification.id,
                        is_read: notification.is_read,
                        message: notification.message
                    }));
                } else if(this.notificationType === 'general') {
                    this.updateNotificationCount();
                }
                else {
                    console.log("Different type of Notification!");
                }
            };

            this.webSocket.onclose = () => {
                console.log('WebSocket connection closed.');
                // implement reconnect logic if desired
            };
        },
        /* This will reset the notification count setting all the unseen notifications 
        as seen */
        toggleNotificationMenu() {
            this.showNotifications = !this.showNotifications;
            //console.log("Notification count:" + this.notificationCount)
            if(this.showNotifications && this.notificationCount > 0){
                this.webSocket.send(JSON.stringify({
                    type: "mark.all.seen",
                    notificationType: this.notificationType
                }));
            }
        },
        /* This method is called when the user clicks on a single notification to mark it as read */
        handleMarkAsRead(id){
            this.webSocket.send(JSON.stringify({
                type: "mark.one.read",
                id: id,
                notificationType: this.notificationType
            }));
        },
        // This will mark all the notifications as read
        handleMarkAllRead(){
            this.webSocket.send(JSON.stringify({
                type: "mark.all.read",
                notificationType: this.notificationType
            }));
        },
        // This will update the notification counter.
        updateNotificationCount() {
            // Send a message to the WebSocket server to request updated notification count
            this.webSocket.send(JSON.stringify({
                type: "update.notification.count",
                notificationType: this.notificationType
            }));
        },
    },
};
</script>
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

.bell {
  display: inline-block;
  margin-top: 5px;
}
</style>