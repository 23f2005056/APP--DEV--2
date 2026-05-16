<template>
    <div class="container mt-4">
      <h3 class="text-center">Unflagged Users</h3>
      <div class="row">
        <!-- Sponsors Section -->
        <div class="col-md-6">
          <h4>Sponsors</h4>
          <ul class="list-group">
            <li class="list-group-item d-flex justify-content-between align-items-center" v-for="user in $store.state.sponsor" :key="user.id">
              <div>
                <strong>{{ user }}</strong>
                <p>{{ user.email }}</p>
                <p>{{ user.industry }}</p>
                <p>fdasdf</p>
              </div>
              <a class="pointer-on-hover text-danger" @click="flag(user.id)">falg</a>
            </li>
          </ul>
        </div>
  
        <!-- Influencers Section -->
        <div class="col-md-6">
          <h4>Influencers</h4>
          <ul class="list-group">
            <li class="list-group-item d-flex justify-content-between align-items-center" v-for="user in $store.state.influencer" :key="user.id">
              <div>
                <strong>{{ user.email }}</strong>
                <p>{{ user.platform }}</p>
                <p>{{ user.fllowers }}</p>
                </div>
              <a class="pointer-on-hover text-danger" @click="flag(user.id)">flag</a>
            </li>

          </ul>
        </div>
      </div>
    </div>
  </template>






<script>
export default {
  data() {
    return {
      sponsors: [], // Sponsors with additional details
      influencers: [], // Influencers with additional details
    };
  },
  methods: {
    async flag(userId) {
      if(confirm("Are you sure?")){
        try {
          const response = await fetch(`http://127.0.0.1:5000/flag/user/${userId}`,{
            method: 'PUT',
            mode: 'cors',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + localStorage.getItem('jwt')
            },
          });
          if (response.status === 201) {
            const data = await response.json();
            console.log(data, "printed data")
            this.$store.commit('updateCategory', data.resource)
            console.log(data.resource)
            this.closeCard()
          } else {
            const data = await response.json();
            alert(data.message);
            console.log(this.$route.params.id)
          }
        } catch (error) {
          console.error(error);
        }
      }
    },
  },
  mounted() {
    this.$store.dispatch('fetchUnflaggedinfluencer')
    this.$store.dispatch('fetchUnflaggedsponsor')
  },
};
</script>


















