<template>
  <div id="app">
    <div id="wrapper">
      <NotificationBell :notificationType="notificationType" />
    </div>
  </div>
</template>

<script>
import NotificationBell from './components/NotificationBell.vue';

export default {
  props: ['notificationType'],
  mounted(){
    console.log('Received notificationType in App.js:', this.notificationType);
  },
  components: {
    NotificationBell,
  }
};
</script>
