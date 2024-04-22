<template>
  <div class="notifications-wrapper" @click="handleMenuClick">
    <div class="notifications-list">
      <a href="#" @click="markAllRead">Mark All as Read</a>
      <ul>
        <li v-for="(notification, index) in notifications.slice(0, 10)" :key="index">
          <div :class="{ 'notification': true, 'bold': !notification.is_read }">
            <div @mouseover="handleMouseOver" @mouseleave="handleMouseLeave" @click="markAsRead(notification)">{{ notification.message}}</div>
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
    props: ['notifications'],
    data() {
        return {
            visibleNotifications: [],
            showMoreLink: false,
        };
    },
    mounted() {
      document.addEventListener('click', this.handleClickOutside);
    },
    beforeUnmount() {
      document.removeEventListener('click', this.handleClickOutside);
    },
    methods: {
        showAllNotifications() {
            // To be implemented
        },
        handleMenuClick(event) {
            event.stopPropagation(); // Prevent the click event from bubbling up
        },
        markAllRead(){
          if(this.areAnyUnread()){
            console.log("There are unread notifications.")
            this.$emit('mark-all-read');
          }else{
            console.log("All the notifications are already read.")
          }
        },
        areAnyUnread(){
          // Check if there is at least one notification with is_read = false
          /*It returns true if at least one notification has is_read set to false, indicating that there are unread notifications.*/
          return this.notifications.some(notification => !notification.is_read);
        },
        markAsRead(notification) {
          /* Only send the action if the notification is set to unread */
          if (!notification.is_read) {
            console.log("The notification type is "+notification)
            this.$emit('mark-as-read', notification.id); // Emit an event to notify the parent component
          }
        },
        handleClickOutside(event) {
          if (!this.$el.contains(event.target)) {
            this.visibleNotifications = [];
            this.showMoreLink = false;
          }
        },
        handleMouseOver(event) {
          event.target.closest('li').querySelector('.notification').classList.add('hovered');
          event.target.closest('li').querySelector('.notification').style.cursor = 'pointer';
        },
        handleMouseLeave(event) {
          event.target.closest('li').querySelector('.notification').classList.remove('hovered');
          event.target.closest('li').querySelector('.notification').style.cursor = 'default';
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
      left: -15;
      width: 300px;   
      max-height: 80vh;
      overflow-y: auto;
      border: 1px solid #ccc;
      border-radius: 5px;
      margin:0;padding:0;
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
      margin: 5px 5px 5px 5px;
      padding: 5px;
      background-color: #fff;
      border: 1px solid #e5e5e5;
      border-radius: 3px;
  }

  .notification.hovered {
    /*background-color: */
    background-color:#f5f5f5;
  }

  .bold {
    font-weight: bold;
  }

  </style>
  