<template>
    <div class="fancy-container">
        <a href="#" class="position-relative">
            <i class="fa fa-bell _gray" style="font-size:24px"></i>
            <!-- <span class="my-text btnLnk">{% translate "Visits" %}</span> -->
            <span class="my-text btnLnk">Visits</span>
            <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger _reduced">
                {{ notificationCount }}
            </span>
        </a>
    </div>
</template>
<script>
    import Axios from 'axios';
    export default{
        data() {
            return {
                notificationCount: 0,
                ws: null,
            };
        },
        created(){
            this.connectWebSocket();
        },
        mounted() {
            this.fetchNotificationCount();
        },
        methods:{
            connectWebSocket(){
                this.ws = new WebSocket('ws://127.0.0.1:8001/websocket/ws/notifications/');
                this.ws.onopen = () => {
                    console.log('WebSocket connected');
                };
                this.ws.onmessage = (event) => {
                    const notification = JSON.parse(event.data);
                    if (notification.is_read === 0) {
                        this.notificationCount += 1;
                    }
                };
                this.ws.onclose = () => {
                    console.log('WebSocket closed. Reconnecting...');
                    setTimeout(this.connectWebSocket, 3000); // Reconnect after 3 seconds
                };
                this.ws.onerror = (error) => {
                    console.error('WebSocket error:', error);
                };
            },
            beforeDestroy() {
                if (this.ws) {
                this.ws.close();
                }
            },
            
            async fetchNotificationCount() {
                try {
                    const response = await Axios.get('http://127.0.0.1:8000/api/process-json/')
                    const unreadNotifications = response.data.filter(notification => notification.is_read === 0);
                    this.notificationCount = unreadNotifications.length;
                }catch(error){
                    console.error('Error fetching notification count:',error);
                }
            },
        },
    };
</script>