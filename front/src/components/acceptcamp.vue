<template>
    <div class="row justify-content-center m-3 text-color-light">
      <div class="card bg-light" style="width: 18rem;">
        <div class="card-body">
          <h5 class="card-title">Accept Campaign</h5>
          <p>Are you sure you want to accept the campaign <strong>?</strong></p>
          <div class="d-flex">
            <button  class="btn btn-outline-success me-2" @click="acceptCampaign(campaign.id)">Yes</button>
            <a class="btn btn-outline-danger" @click="goBack">No</a>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        campaign: null, // Will hold the fetched campaign data
      };
    },
    methods: {
      goBack() {
        this.$router.push('/influ'); // Or redirect to any page you want
      },
      async fetchCampaign() {
        try {
          const response = await fetch('http://127.0.0.1:5000/get/campaign/'+this.$route.params.id, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + localStorage.getItem('jwt')
            }
          });
  
          if (response.status === 200) {
            const data = await response.json();
            this.campaign = data.campaign; 
          } else {
            alert('Failed to fetch campaign.');
          }
        } catch (error) {
          console.error(error);
        }
      },



      async acceptCampaign(id) {
            if (confirm("Are you sure you want to accept this campaign?")) {
                try {
                const response = await fetch('http://127.0.0.1:5000/accept/campaign/${id}', {
                    method: 'PUT',
                    mode: 'cors',
                    credentials: 'include',
                    headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('jwt')
                    },
                });

                if (response.status === 200) {
                    const data = await response.json();
                    console.log("Campaign accepted:", data);
                    
                    // Update the store
                    this.$store.commit('updateYourCamp', data.campaign); // Assuming the accepted campaign is returned in `data.campaign`
                    this.$store.commit('deleteCampaign', data.campaign.id); // Remove accepted campaign from the 'others' list

                    // Redirect after accepting the campaign
                    this.$router.push('/influ'); // Redirect to the manager page
                } else {
                    const data = await response.json();
                    alert(data.message);
                }
                } catch (error) {
                console.error(error);
                }
            }
        }
},

    mounted() {
      this.fetchCampaign(); // Fetch campaign details when the component is mounted
    }
  }
  </script>
  