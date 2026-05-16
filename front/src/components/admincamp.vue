<template>
    <div class="container mt-4">
      <h3 class="text-center">Current Campaigns</h3>
      <ul class="list-group">
        <li class="list-group-item d-flex justify-content-between align-items-center" v-for="campaign in $store.state.campaigns" :key="campaign.id">
          <div>
            <strong>{{ campaign.name }}</strong>
            <span class="d-block">budget-{{ campaign.budget }}, enddate -{{ campaign.end_date }}, sponsor -{{ campaign.sponsor }}, influencer -{{ campaign.influencer }}</span>
          </div>
          <a class="pointer-on-hover text-danger" @click="deleteCampaign(campaign.id)">Delete</a>
        </li>

    </ul>
    </div>
  </template>


<script>
export default {
  data() {
    return {
      campaigns: [], // Array to store current campaigns
    };
  },
  methods: {
    // Fetch all existing campaigns
    // async fetchCampaigns() {
    //   try {
    //     const response = await fetch("http://127.0.0.1:5000/get/current-campaigns", {
    //       method: "GET",
    //       mode: "cors",
    //       credentials: "include",
    //       headers: {
    //         "Content-Type": "application/json",
    //         Authorization: "Bearer " + localStorage.getItem("jwt"),
    //       },
    //     });

    //     if (response.status === 200) {
    //       const data = await response.json();
    //       console.log(data, 'campaigns fetched');
    //       commit('setCampaigns', data);
    //     } else {
    //       alert("Failed to fetch campaigns");
    //     }
    //   } catch (error) {
    //     console.error(error);
    //   }
    // },

    // Delete a campaign
    async deleteCampaign(campaignId) {
      if (confirm("Are you sure you want to delete this campaign?")) {
        try {
          const response = await fetch(`http://127.0.0.1:5000/delete/campaign/${campaignId}`, {
            method: "DELETE",
            mode: "cors",
            credentials: "include",
            headers: {
              "Content-Type": "application/json",
              Authorization: "Bearer " + localStorage.getItem("jwt"),
            },
          });

          if (response.status === 200) {
            const data = await response.json();
            alert("Campaign deleted successfully!");
            // Remove the deleted campaign from the list
            this.campaigns = this.campaigns.filter(campaign => campaign.id !== campaignId);
          } else {
            const data = await response.json();
            alert("Failed to delete campaign: " + data.message);
          }
        } catch (error) {
          console.error(error);
        }
      }
    },
  },
  mounted() {
    // Fetch campaigns when the component is mounted
    this.$store.dispatch('fetchCampaignsall');
  },
};
</script>



