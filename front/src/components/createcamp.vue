<template>
    <div class="row justify-content-center m-3 text-color-light">
      <div class="card bg-light" style="width: 36rem;">
        <div class="card-body">
          <h5 class="card-title">Add Campaign</h5>
          <form @submit.prevent="addCampaign">
            <label class="form-label" for="title">Campaign Name:</label>
            <input class="form-control" v-model="campaign.name" type="text" id="title" name="title" required />
            <br />
  


            <!-- <label class="form-label" for="title">Title:</label>
            <textarea
              class="form-control"
              v-model="campaign.description"
              type="text"
              id="title"
              name="title"
              required
            ></textarea> -->

            <label class="form-label" for="description">Description:</label>
            <textarea
              class="form-control"
              v-model="campaign.description"
              type="text"
              id="description"
              name="description"
              required
            ></textarea>
            <br />
  
            <label class="form-label" for="enddate">End Date:</label>
            <input
              class="form-control"
              v-model="campaign.enddate"
              type="date"
              id="enddate"
              name="enddate"
              required
            />
            <br />
  
            <label class="form-label" for="budget">Budget:</label>
            <input
              class="form-control"
              v-model="campaign.budget"
              type="number"
              id="budget"
              name="budget"
              step="0.01"
              required
            />
            <br />
  
            <input type="submit" class="btn btn-outline-primary" value="Add Campaign" />
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        campaign: {
          title: "",
          description: "",
          enddate: "",
          budget: 0,
        },
      };
    },
    methods: {
      async addCampaign() {
        const formData = new FormData();
        formData.append("title", this.campaign.title);
        formData.append("description", this.campaign.description);
        formData.append("enddate", this.campaign.enddate);
        formData.append("budget", this.campaign.budget);
  
        try {
          const response = await fetch("http://127.0.0.1:5000/spon/camp/add", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": "Bearer " + localStorage.getItem("jwt") ,
              'X-User-Email': localStorage.getItem('email')
            },
            body: JSON.stringify(this.campaign),
          });

          if (response.status === 201) {
            const data = await response.json();
            console.log(data.resource);
            if (this.$store.state.authenticatedUser.role === "spon") {
              this.$store.commit("addCampaign", data.resource);
            } else {
              this.$store.commit("addNoti", data.resource);
            }
            this.closeCard();
          } else if (response.status === 409) {
            const data = await response.json();
            alert(data.message);
          } else {
            alert("An error occurred while adding the campaign.");
          }
          this.$router.push('/influ/report')
        } catch (error) {
          console.error(error);
        }
      },
    },
  };
  </script>
  