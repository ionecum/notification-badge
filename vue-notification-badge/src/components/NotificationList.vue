<template>
    <div class="notifications-list">
      <ul>
        <li v-for="(notification, index) in notifications" :key="index">
        {{ notification.message }}
      </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    props: ['notifications'],
    mounted() {
      console.log('Notifications in child component:', this.notifications);
    }
  };
  </script>
  
  <style>
  .notifications-list {
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 10px;
    background-color: #f9f9f9;
  }
  .notifications-list ul {
    list-style-type: none;
    padding: 0;
  }
  .notifications-list li {
    margin-bottom: 5px;
    padding: 5px;
    background-color: #fff;
    border: 1px solid #e1e1e1;
    border-radius: 3px;
  }
  </style>
  