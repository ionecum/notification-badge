<template>
  <div class="notifications-wrapper" @click.stop>
    <div class="notifications-list">
      <a v-if="areAnyUnread" href="#" @click="markAllRead">Mark All as Read</a>
      <ul>
        <li v-for="(notification, index) in notifications.slice(0, 10)" :key="index">
          <div class="notification" :class="{ 'bold': !notification.is_read }" @click="markAsRead(notification)">
            {{ notification.message}}
          </div>
        </li>
      </ul>
      <div v-if="notifications.length > 10" class="see-more-link">
        <a href="#" @click="showAllNotifications">See More</a>
      </div>
    </div>
  </div>
</template>
<script>
  export default {
    props: {
        notifications: {
            type: Array,
            required: true
        }
    },
    data() {
        return {
            visibleNotifications: [], // You are not using this property, you can delete it.
            showMoreLink: false, // You are not using this property, you can delete it.
        };
    },
    computed: {
        areAnyUnread(){
            // Check if there is at least one notification with is_read = false
            /*It returns true if at least one notification has is_read set to false, indicating that there are unread notifications.*/
            return this.notifications.some(notification => !notification.is_read);
        }
    },
    methods: {
        showAllNotifications() {
            // To be implemented
        },
        markAllRead(){
          if(this.areAnyUnread){
            //console.log("There are unread notifications.")
            this.$emit('mark-all-read');
          }else{
            console.log("All the notifications are already read.")
          }
        },
        markAsRead(notification) {
          /* Only send the action if the notification is set to unread */
          if (!notification.is_read) {
            //console.log("The notification type is "+notification)
            this.$emit('mark-as-read', notification.id); // Emit an event to notify the parent component
          }
        }
    },
  };
</script>
<style>
.notifications-wrapper {
  position: relative;
  display: inline-block;
}

.notifications-list {
  position: absolute;
  top: 100%;
  left: -15px;
  width: 300px;
  max-height: 80vh;
  overflow-y: auto;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin: 0;
  margin-top:5px;
  padding: 0;
  background-color: #FBFBFB;
}

.see-more-link {
  margin: 10px 0;
}

.notifications-list ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.notifications-list li {
  margin: 5px;
  padding: 5px;
  background-color: #fff;
  border: 1px solid #e5e5e5;
  border-radius: 3px;
}

.notification:hover {
  /*background-color: */
  background-color: #f5f5f5;
  cursor: pointer;
}

.bold {
  font-weight: bold;
}
</style>
  