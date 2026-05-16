<template>
    <div class="row justify-content-center m-3 text-color-light">
      <div class="card bg-light" style="width: 18rem;">
        <div class="card-body">
          <h5 class="card-title">Edit Campaign</h5>
          <form @submit.prevent="updateCampaign">
            <div class="mb-3">
              <label for="title" class="form-label">Campaign Title</label>
              <input type="text" class="form-control" v-model="title" required>
            </div>

            <div class="mb-3">
              <label for="description" class="form-label">Description</label>
              <textarea class="form-control" v-model="description" rows="3" required></textarea>
            </div>

            <div class="mb-3">
              <label for="end_date" class="form-label">End Date</label>
              <input type="date" class="form-control" v-model="end_date" required>
            </div>

            <div class="mb-3">
              <label for="budget" class="form-label">Budget</label>
              <input type="number" class="form-control" v-model="budget" required>
            </div>

            <div v-if="message" class="alert alert-warning">
              {{ message }}
            </div>
            <div class="d-flex">
              <button type="submit" class="btn btn-outline-primary me-5">Update</button>
              <a class="btn btn-outline-danger" @click="deleteCampaign">Delete</a>
            </div>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        title: '',
        description: '',
        budget: null,
        message: '',
      };
    },
    methods: {
      async fetchCampaign() {
        try {
          const response = await fetch('http://127.0.0.1:5000/get/campaign/' + this.$route.params.id, {
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
            this.title = data.title;
            this.description = data.description;
            this.budget = data.budget;
          } else if (response.status === 404) {
            alert(data.message);
          }
        } catch (error) {
          console.error(error);
        }
      },
      async updateCampaign() {
        if (confirm('Are you sure?')) {
          try {
            // const formData = new FormData();
            //     formData.append("title", this.campaign.title);
            //     formData.append("description", this.campaign.description);
            //     formData.append("budget", this.campaign.budget);
            //     formData.append("end_date", this.campaign.end_date);
            const response = await fetch('http://127.0.0.1:5000/update/campaign/' + this.$route.params.id, {
              method: 'PUT',
              mode: 'cors',
              credentials: 'include',
              headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + localStorage.getItem('jwt'),
              },
              body: JSON.stringify({
                title: this.title,
                description: this.description,
                budget: this.budget,
              }),
            });
            if (response.status === 201) {
              const data = await response.json();
              if (this.$store.state.authenticatedUser.role === 'spon') {
                this.$store.commit('updateCampaign', data.resource);
              } else {
                this.$store.commit('addNoti', data.resource);
              }
              this.closeCard();
            } else {
              const data = await response.json();
              alert(data.message);
            }
          } catch (error) {
            console.error(error);
          }
        }
      },
      async deleteCampaign() {
        if (confirm('Are you sure?')) {
          try {
            const response = await fetch('http://127.0.0.1:5000/delete/campaign/' + this.$route.params.id, {
              method: 'DELETE',
              mode: 'cors',
              credentials: 'include',
              headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + localStorage.getItem('jwt'),
              },
            });
            if (response.status === 201) {
              const data = await response.json();
              if (this.$store.state.authenticatedUser.role === 'spon') {
                this.$store.commit('deleteCampaign', data.resource.id);
              } else {
                this.$store.commit('addNoti', data.resource);
              }
              this.closeCard();
            } else {
              const data = await response.json();
              alert(data.message);
            }
          } catch (error) {
            console.error(error);
          }
        }
      },
    },
    mounted() {
      this.fetchCampaign();
    },
  };
  </script>
  