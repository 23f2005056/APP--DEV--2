<template>
    <div class="row justify-content-center m-3 text-color-light">
      <div class="card bg-light" style="width: 36rem;">
        <div class="card-body">
          <h5 class="card-title">Associated Influencers</h5>
  
          <ul class="list-group">
            <li 
              v-for="influencer in this.$store.state.influencers" 
              :key="influencer.id" 
              class="list-group-item"
            >
              <div class="d-flex justify-content-between align-items-center">
                <!-- Influencer Details in a Single Line -->
                <div>
                  <strong>{{ influencer.name }}</strong> | 
                  Platform: {{ influencer.platform }} | 
                  Followers: {{ influencer.followers }}
                </div>
  
                <!-- Assign Button -->
                <div>
                  <button 
                    class="btn btn-outline-primary btn-sm pointer-on-hover" 
                    @click="assignInfluencer(influencer.id)"
                  >
                    Assign
                  </button>
                </div>
              </div>
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
        influencersList: [], // To store influencers associated with campaigns
      };
    },
    methods: {
        
      // Fetch influencers associated with campaigns
      async fetchInfluencers() {
        try {
          const response = await fetch('http://127.0.0.1:5000/campaigns/influencers'+this.$route.params.id, {
            method: 'GET',
            headers: {
              Authorization: 'Bearer ' + localStorage.getItem('jwt'),
              'Content-Type': 'application/json',
            },
          });
  
          if (response.status === 200) {
            const data = await response.json();
            this.$store.commit('setInfluencer', data.influencers);
            console.log(data.influencers);
          } else {
            const data = await response.json();
            alert(data.message);
          }
        } catch (error) {
          console.error(error);
        }
      },
  
      // Assign an influencer to a campaign
      async assignInfluencer(influencerId) {
        if (confirm("Are you sure you want to assign this influencer to the campaign?")) {
          try {
            const response = await fetch(`http://127.0.0.1:5000/assign/influencer/${influencerId}/campaign/${this.$route.params.campaignId}`, {
              method: 'POST',
              headers: {
                Authorization: 'Bearer ' + localStorage.getItem('jwt'),
                'Content-Type': 'application/json',
              },
            });
  
            if (response.status === 201) {
              alert("Influencer successfully assigned!");


            } else {
              const data = await response.json();
              alert(data.message);
            }

          } catch (error) {
            console.error(error);
          }
          this.$router.push('/spon')
        }
      },
    },
    mounted() {
      this.fetchInfluencers(); // Fetch the influencers when the component is mounted
    },
  };
  </script>
  