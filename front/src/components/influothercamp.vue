<template>
    <div class="row justify-content-center m-3 text-color-light">
      <div class="card bg-light" style="width: 36rem;">
        <div class="card-body">
          <h5 class="card-title">Other Campaigns</h5>



            <ul class="list-group">
              <li v-for="campaign in this.$store.state.othercamp" :key="campaign.id" class="list-group-item">
                <div class="d-flex justify-content-between">

                  <div>
                  <strong>{{ campaign.title }}</strong><br>
                  <span>{{ campaign.budget }}</span><br>
                  <span>{{ campaign.description }}</span>
                  <span>{{ campaign.end_date }}</span>
                  </div>

                  <div>
                  <button class="btn btn-outline-primary btn-sm pointer-on-hover" @click="acceptcamp(campaign.id)">
                  acceptcamp
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
        campaigns: [], // To store campaigns that do not belong to the sponsor
      };
    },
    methods: {
      async fetchNoninfluencerCampaigns() {
          try {
              const email = localStorage.getItem('email'); // Get the logged-in influencer's email
              const response = await fetch(`http://127.0.0.1:5000/campaigns/others`, {
                  method: 'POST',
                  headers: {
                      'Authorization': 'Bearer ' + localStorage.getItem('jwt'),
                      'Content-Type': 'application/json',
                  },
                  body: JSON.stringify({ email }), // Pass email in request body
              });

              if (response.status === 200) {
                  const data = await response.json();
                  this.$store.commit('setOtherCamp', data.campaigns);
              } else {
                  const data = await response.json();
                  alert(data.message);
              }
          } catch (error) {
              console.error(error);
          }
      },

      // View a specific campaign's details
      // acceptcamp(campaignId) {
      //   this.$router.push('/influ/camp/accep/'+campaignId);
      // }


  async acceptcamp(id) {
    try {
      const email = localStorage.getItem('email'); // Get the logged-in influencer's email
      console.log(id)
      const response = await fetch(`http://127.0.0.1:5000/campaigns/accept/${id}`, {
        mode: "cors",
        method: 'PUT',
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem('jwt'),
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }) // Send email and campaignId
      });


      if (response.status === 200) {
        const data = await response.json();
        // Update the state after accepting the campaign
        this.$store.commit('updateAccepCamp', data.updatedCampaign);
        // Remove the campaign from othercamp state after accepting
        this.$store.commit('deleteOtherCamp', campaignId);
        alert('Campaign accepted successfully!');
      } else {
        const data = await response.json();
        alert(data.message);
      }
    } catch (error) {
      console.error(error);
    }
  }
},


  mounted() {
      this.fetchNoninfluencerCampaigns(); // Fetch the campaigns when the component is mounted
    }
  };
  </script>
  