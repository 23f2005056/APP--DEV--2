<template>
    <div class="container">
      <div class="row">
        <!-- Loop through each completion request -->
        <div v-for="item in this.$store.state.completions" class="col-md-6">
          <div class="completion-item">
            <!-- Proof View -->
            <h5>{{ item.campaign_name }} - Proof</h5>
            <div v-if="item.proof">
              <img :src="item.proof" alt="Completion Proof" />
            </div>
            <p v-else>No proof available</p>
  
            <!-- Action Buttons -->
            <div class="action-buttons">
              <button @click="approve(item.id)">Approve</button>
              <button @click="reject(item.id)">Reject</button>
            </div>
          </div>
        </div>
        <!-- Message if no completions are available -->
        <div v-if="this.$store.state.completions.length == 0">
          <h5>No completion requests</h5>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      
      async fetchCompleConfirmCap() {
        try {
          const response = await fetch('http://127.0.0.1:5000/get/compleconfirmcap', {
            method: 'GET',
            mode: 'cors',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
              Authorization: 'Bearer ' + localStorage.getItem('jwt'),
            },
          });
          if (response.status === 200) {
            const data = await response.json();
            this.$store.commit('campcompleconfirm/setCompleConfirmCap', data);
          } else if (response.status === 404) {
            const data = await response.json();
            alert(data.message);
          }
        } catch (error) {
          console.error(error);
        }
      },


      async reject(id) {
        try {
          const response = await fetch(`http://127.0.0.1:5000/reject/completion/${id}`, {
            method: 'POST',
          });
          if (response.status === 200) {
            const data = await response.json();
            this.$store.commit('removeCompletion', id); // Remove rejected completion from Vuex store
            alert(data.message);
          } else {
            const data = await response.json();
            alert(data.message);
          }
        } catch (error) {
          console.error(error);
        }
      },
  
      // Handle approve action (send approval request to the server)
      async approve(id) {
        try {
          const response = await fetch(`http://127.0.0.1:5000/approve/completion/${id}`, {
            method: 'POST',
          });
          if (response.status === 200) {
            const data = await response.json();
            this.$store.commit('updateCompletionStatus', { id, status: 'approved' }); // Update completion status in Vuex
            alert(data.message);
          } else {
            const data = await response.json();
            alert(data.message);
          }
        } catch (error) {
          console.error(error);
        }
      },
    },
  };
  </script>
  