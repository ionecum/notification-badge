import { createApp, h } from 'vue'
import App from './App.vue'

let notificationTypes = [];
//  This will retrieve a NodeList of all elements that have the class bell.
const bellElements = document.querySelectorAll('.bell');
bellElements.forEach(element => {
    const notificationType = element.dataset.notificationType;
    notificationTypes.push(notificationType); 
    //console.log(notificationType)
    // Mount the App component with the corresponding notification type
    createApp({
      render: () => h(App, { notificationType: notificationType })
    }).mount(`#${element.id}`);
  });


