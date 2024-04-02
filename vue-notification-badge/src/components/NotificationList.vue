<template>
  <div class="notifications-wrapper" @click="handleMenuClick">
    <div class="notifications-list">
      <a href="#">Mark All as Read</a>
      <ul>
        <li v-for="(notification, index) in notifications.slice(0, 10)" :key="index">
          <div :class="{ 'notification': true, 'bold': !notification.is_read }">
            {{ notification.message }}
            
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
            // Show all notifications when 'See More' is clicked
            this.visibleNotifications = this.notifications;
            this.showMoreLink = false; // Hide 'See More' link after displaying all notifications
        },
        handleMenuClick(event) {
            event.stopPropagation(); // Prevent the click event from bubbling up
        },
        markAsRead(notification) {
            notification.is_read = true;
        },
        handleClickOutside(event) {
          if (!this.$el.contains(event.target)) {
            this.visibleNotifications = [];
            this.showMoreLink = false;
          }
        },
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
      background-color: #f9f9f9;
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
      margin-bottom: 5px;
      padding: 5px;
      background-color: #fff;
      border: 1px solid #e1e1e1;
      border-radius: 3px;
  }
  .bold {
    font-weight: bold;
  }

  </style>
  